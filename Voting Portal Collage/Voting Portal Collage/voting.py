from flask import Flask, request, jsonify, Blueprint, current_app,render_template
from web3 import Web3
import json
import os
from config import Config as conf
from ajaxController import createElection
import db
from redisConn import redisConnection
from ajaxController import saveElectionResult


ganache_url = conf.BLOCKCHAIN_URL
w3 = Web3(Web3.HTTPProvider(ganache_url))

if not w3.is_connected():
    raise Exception("Failed to connect to Ganache. Make sure Ganache is running!")

default_account = w3.eth.accounts[1]
w3.eth.default_account = default_account

# Load contract ABI and address
with open('contract_abi.json', 'r') as f:
    contract_abi = json.load(f)

# Replace with your deployed contract address
contract_address = os.environ.get('CONTRACT_ADDRESS', conf.BLOCKCHAIN_CONTRACT_ADDRESS)
contract = w3.eth.contract(address=contract_address, abi=contract_abi)
# Define the blueprint for voting
voting_bp = Blueprint('voting', __name__)

@voting_bp.route('/create-election', methods=['POST'])
def create_election():
    try:
        data = request.get_json()
        
        createFlag = data['createFlag']
        # print(electionName)
        # print(electionDate)
        # print(positionList)
        # candidate_list=[]
        position_list=[]
        election_id = None
    
        if createFlag == 'create':
            electionName = data['electionName']
            electionDate = data['electionDate']
            positionList = data['positionList']
            election_id,position_list = createElection.createElection(db.get_connection(), electionName, electionDate, positionList)
        else:
            election_id = data['electionId']
            position_list = data['positionList']
            # candidate_list = data['candidateList']
        if election_id is None:
            return jsonify({'statusCode': 400, 'message': 'Failed to create election.'}), 200
        
        # Prepare data for smart contract
        position_ids = []
        candidate_ids_nested = []
        
        for position in position_list:
            position_ids.append(position['positionId'])
            
            candidates = []
            for candidate in position['candidateList']:
                candidates.append(candidate)
            
            
            
            candidate_ids_nested.append(candidates)
        
        # Call smart contract function
        tx_hash = contract.functions.createOrUpdateElection(
            election_id,
            position_ids,
            candidate_ids_nested
        ).transact({'from': default_account})
        
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Check if this was a new election or an update
        is_new = False
        try:
            # Try to get positions - if it fails, it's a new election
            contract.functions.getElectionPositions(election_id).call()
            is_new = False
        except:
            is_new = True
        
        message = "Election created successfully" if is_new else "Election updated successfully"
        
        return jsonify({
            'statusCode': 200,
            'message': message,
            'transactionHash': tx_hash.hex(),
            'blockNumber': tx_receipt['blockNumber']
        }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@voting_bp.route('/cast-vote', methods=['POST'])
def cast_vote():
    try:
        data = request.get_json()
        election_id = data['electionId']
        position_id = data['positionId']
        candidate_id = data['candidateId']
        userId = data['userId']

        user_vote_key = f"user_vote:{userId}:{election_id}:{position_id}"
        # redisConnection.delete(user_vote_key)
        # vote_data = redisConnection.rpop("vote_queue")
        if redisConnection.exists(user_vote_key):
            return jsonify({"message": "You have already voted for this position","statusCode":403}),200
        
        # Call smart contract function
        tx_hash = contract.functions.castVote(
            election_id,
            position_id,
            candidate_id
        ).transact({'from': default_account})
        
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        redisConnection.setex(user_vote_key, 86400, user_vote_key)
        return jsonify({
            'statusCode': 200,
            'message': 'Vote casted successfully',
            'transactionHash': tx_hash.hex(),
            'blockNumber': tx_receipt['blockNumber']
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@voting_bp.route('/vote_results', methods=['POST'])
def vote_result():
    try:
        election_id = request.get_json()['electionId']
        result = get_voting_results(election_id)
        return  jsonify({"statusCode":200,"data":result})  # Render admin dashboard
    except Exception as e:
        return  jsonify({"statusCode":400,"data":{}})  # Render admin dashboard




def get_voting_results(election_id):
    try:
        # electionDetails = db.execute_query("select * from vote.elections where status='ACTV'")
        # if len(electionDetails) ==0 or electionDetails is None :
        #     print("no election")
        #     return  render_template('admin/votingResult.html',results={})  # Render admin dashboard
        # election_id = electionDetails[0]['election_id']
        # print("election_id",election_id)
        # Get position IDs for the election
        position_ids = contract.functions.getElectionPositions(election_id).call()
        
        # Prepare result data
        result = {
            'electionId': election_id,
            'positionList': []
        }

       
        
        # Get candidates and vote counts for each position
        for position_id in position_ids:
            candidates = contract.functions.getCandidates(election_id, position_id).call()
            
            candidate_list = []
            for candidate in candidates:
                candidate_list.append({
                    'candidateId': candidate[0],
                    'voteCount': candidate[1]
                })
            
            result['positionList'].append({
                'positionId': position_id,
                'candidateList': candidate_list
            })
        
        return result
    except Exception as e:
        return  {}
        

@voting_bp.route('/check-candidate', methods=['GET'])
def check_candidate():
    try:
        election_id = int(request.args.get('electionId'))
        position_id = int(request.args.get('positionId'))
        candidate_id = int(request.args.get('candidateId'))
        
        exists = contract.functions.checkCandidateExists(
            election_id,
            position_id,
            candidate_id
        ).call()
        
        return jsonify({
            'exists': exists
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@voting_bp.route('/export-to-database', methods=['POST'])
def export_to_database():
    try:
        election_id = request.get_json().get('electionId')
        
        # Get election results from blockchain
        position_ids = contract.functions.getElectionPositions(election_id).call()
        
        # Prepare result data
        result = {
            'electionId': election_id,
            'positionList': []
        }
        
        # Get candidates and vote counts for each position
        for position_id in position_ids:
            candidates = contract.functions.getCandidates(election_id, position_id).call()
            
            candidate_list = []
            for candidate in candidates:
                candidate_list.append({
                    'candidateId': candidate[0],
                    'voteCount': candidate[1]
                })
            
            result['positionList'].append({
                'positionId': position_id,
                'candidateList': candidate_list
            })
        
        status = saveElectionResult.save_election_results(db.get_connection(),result)
        
        return status, 200
    
    except Exception as e:
        return jsonify({
            'statusCode': 400,
            'message': str(e)
        }), 200



if __name__ == '__main__':
    current_app.run(debug=True)

