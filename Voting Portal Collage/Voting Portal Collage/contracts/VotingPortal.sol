// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingPortal {
    struct Candidate {
        uint candidateId;
        uint voteCount;
    }

    struct Position {
        uint positionId;
        mapping(uint => uint) candidateIndex; // candidateId => index in candidates array
        Candidate[] candidates;
        bool exists;
    }

    struct Election {
        uint electionId;
        mapping(uint => Position) positions; // positionId => Position
        uint[] positionIds;
        bool exists;
    }

    mapping(uint => Election) public elections;
    uint[] public electionIds;

    event ElectionCreated(uint electionId);
    event ElectionUpdated(uint electionId);
    event VoteCasted(uint electionId, uint positionId, uint candidateId);

    function createOrUpdateElection(uint electionId, uint[] memory positionIds, uint[][] memory candidateIds) public {
        bool isNewElection = !elections[electionId].exists;
        
        if (isNewElection) {
            // Create new election
            elections[electionId].electionId = electionId;
            elections[electionId].exists = true;
            electionIds.push(electionId);
            
            emit ElectionCreated(electionId);
        } else {
            emit ElectionUpdated(electionId);
        }
        
        // Process each position
        for (uint i = 0; i < positionIds.length; i++) {
            uint positionId = positionIds[i];
            
            // Check if position already exists
            if (!elections[electionId].positions[positionId].exists) {
                // Add new position
                elections[electionId].positionIds.push(positionId);
                elections[electionId].positions[positionId].positionId = positionId;
                elections[electionId].positions[positionId].exists = true;
            }
            
            // Process candidates for this position
            for (uint j = 0; j < candidateIds[i].length; j++) {
                uint candidateId = candidateIds[i][j];
                
                // Check if candidate already exists
                if (elections[electionId].positions[positionId].candidateIndex[candidateId] == 0 && 
                    (elections[electionId].positions[positionId].candidates.length == 0 || 
                     elections[electionId].positions[positionId].candidates[0].candidateId != candidateId)) {
                    
                    // Add new candidate
                    elections[electionId].positions[positionId].candidates.push(Candidate({
                        candidateId: candidateId,
                        voteCount: 0
                    }));
                    elections[electionId].positions[positionId].candidateIndex[candidateId] = 
                        elections[electionId].positions[positionId].candidates.length - 1;
                }
                // Note: We don't update existing candidates to preserve vote counts
            }
        }
    }

    // For backward compatibility
    function createElection(uint electionId, uint[] memory positionIds, uint[][] memory candidateIds) public {
        createOrUpdateElection(electionId, positionIds, candidateIds);
    }

    function castVote(uint electionId, uint positionId, uint candidateId) public {
        require(elections[electionId].exists, "Election does not exist");
        require(elections[electionId].positions[positionId].exists, "Position does not exist");
        
        uint candidateIndex = elections[electionId].positions[positionId].candidateIndex[candidateId];
        elections[electionId].positions[positionId].candidates[candidateIndex].voteCount++;
        
        emit VoteCasted(electionId, positionId, candidateId);
    }

    function getElectionPositions(uint electionId) public view returns (uint[] memory) {
        require(elections[electionId].exists, "Election does not exist");
        return elections[electionId].positionIds;
    }

    function getCandidates(uint electionId, uint positionId) public view returns (Candidate[] memory) {
        require(elections[electionId].exists, "Election does not exist");
        require(elections[electionId].positions[positionId].exists, "Position does not exist");
        
        return elections[electionId].positions[positionId].candidates;
    }

    function getElectionIds() public view returns (uint[] memory) {
        return electionIds;
    }

    function checkCandidateExists(uint electionId, uint positionId, uint candidateId) public view returns (bool) {
        if (!elections[electionId].exists || !elections[electionId].positions[positionId].exists) {
            return false;
        }
        
        uint candidateIndex = elections[electionId].positions[positionId].candidateIndex[candidateId];
        if (candidateIndex == 0 && elections[electionId].positions[positionId].candidates.length > 0) {
            return elections[electionId].positions[positionId].candidates[0].candidateId == candidateId;
        }
        
        return candidateIndex > 0;
    }
}

