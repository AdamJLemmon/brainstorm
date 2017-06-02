contract owned {
    address public owner;

    function owned() {
        owner = msg.sender;
    }

    modifier onlyOwner {
        if (msg.sender != owner) throw;
        _;
    }
}

contract HighLowBet is owned {
    // address of contract where lost funds are sent
    address public lt_contract_address;
    // address of account making bet to take/allocate funds
    address public user_address;
    // bet quantity
    uint256 public bet_amount;
    // which card they are on the compute odds
    uint8 public card_number;

    /* This generates a public event on the blockchain that will notify clients */
    event BetPlaced(address user_address, uint256 amount);
    event BetWon(address user_address, uint256 amount);
    event BetLost(address user_address, uint256 amount);

    /* Initializes contract with addresses amount and card number of 0 */
    function HighLowBet(
        address lt_contract_address,
        address user_address,
        uint8 bet_amount
        ) {
        lt_contract_address = lt_contract_address; 

        // TODO: add code of LT contract above in order to instantiate, need abi sig
        // LTGame ltGame = LTGame(lt_contract_address);
        user_address = user_address;   

        // TODO: need to check if the user has at least this amount!!
        // Call lt contract to check if user has enough
        // if the account has enough then subtract the amount from the account
        bet_amount = bet_amount;    
        card_number = 0;

        BetPlaced(user_address, bet_amount);
    }

    function generate_card() onlyOwner returns (uint card) {
        // generate new card
        // generate value 0 - 51
        card = uint(sha3(block.blockhash(block.number-1)))%51;

        // update card number
        card_number += 1;

        return card;
    }

    // function compute_guess(uint8 current_card, bool guess) {
    //     // false is under true is over for simplicity

    //     // generate new card to compare with
    //     // uint8 new_card = random value 0 - 51
    //     // compare new card 

    //     // update card number
    //     // card_number += 1;
    // }


    /* issue bet amount to ltGame */
    function transfer_bet_lost() private returns (bool success) {
        // call to lt contract to transfer lost amount
        BetLost(user_address, bet_amount);
        return true;
    }

    /* issue funds from lt to user when bet won */
    function transfer_bet_won() 
    private returns (bool success) {
        // call to LTGame to update the user's balance
        // multiplier = card_number * some probability computation
        uint256 multiplier = 2;
        uint256 won_amount = bet_amount * multiplier;

        BetWon(user_address, won_amount);

        return true;
    }

    /* This unnamed function is called whenever someone tries to send ether to it */
    function () {
        throw;     // Prevents accidental sending of ether
    }
}