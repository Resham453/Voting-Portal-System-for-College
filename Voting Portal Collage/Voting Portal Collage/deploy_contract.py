from web3 import Web3
import json
import solcx

# Install specific Solidity compiler version
solcx.install_solc('0.8.17')

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if not w3.is_connected():
    raise Exception("Failed to connect to Ganache. Make sure Ganache is running!")

# Set default account
default_account = w3.eth.accounts[1]
w3.eth.default_account = default_account

def compile_contract():
    # Compile the contract
    print("Compiling contract...")
    
    with open('contracts/VotingPortal.sol', 'r') as file:
        contract_source_code = file.read()
    
    compiled_sol = solcx.compile_standard({
        "language": "Solidity",
        "sources": {
            "VotingPortal.sol": {
                "content": contract_source_code
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    }, solc_version="0.8.17")
    
    # Save the compiled contract
    with open('compiled_contract.json', 'w') as file:
        json.dump(compiled_sol, file)
    
    # Extract contract data
    contract_data = compiled_sol['contracts']['VotingPortal.sol']['VotingPortal']
    abi = contract_data['abi']
    bytecode = contract_data['evm']['bytecode']['object']
    
    # Save ABI separately for easier access
    with open('contract_abi.json', 'w') as file:
        json.dump(abi, file)
    
    return abi, bytecode

def deploy_contract(abi, bytecode):
    # Create contract instance
    VotingPortal = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Deploy contract
    print(f"Deploying contract from account: {default_account}")
    tx_hash = VotingPortal.constructor().transact({'from': default_account})
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    
    print(f"Contract deployed at address: {contract_address}")
    
    # Save contract address
    with open('contract_address.txt', 'w') as file:
        file.write(contract_address)
    
    return contract_address

if __name__ == "__main__":
    abi, bytecode = compile_contract()
    contract_address = deploy_contract(abi, bytecode)
    
    print("\nDeployment successful!")
    print(f"Contract Address: {contract_address}")
    print("ABI saved to: contract_abi.json")
    print("Contract address saved to: contract_address.txt")
    print("\nUpdate your app.py with this contract address.")

