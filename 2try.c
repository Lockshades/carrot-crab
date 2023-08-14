#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int user_rebet(userBalance, betAmount)
    {
        printf("Your current balance: ₦%d\n", userBalance);

        // Get user's bet amount and numbers
        printf("Enter your bet amount: ");
        scanf("%d", &betAmount);

        return betAmount;
    }

int main() {
    int userBalance = 10000, betAmount;
    int server_balance = 0; //This is how much the bet company has made
     // Initial user balance, you can change this value as per your requirement.
    int userNumber1, userNumber2, userNumber3;
    int systemNumber1, systemNumber2, systemNumber3;
    char playAgain;

    srand(time(NULL)); // Seed the random number generator with current time

    printf("Welcome to Sapa_money_bet lottery system!\n");

    
    do {
        
        user_rebet(userBalance, betAmount);

        if (betAmount > userBalance)
        {
            int bet_multiplier = 3;
            printf("Enter three different numbers (0 to 100):\n Max multiplier is X5%d\n", bet_multiplier^3);
            printf("Number 1: ");
            scanf("%d", &userNumber1);
            printf("Number 2: ");
            scanf("%d", &userNumber2);
            printf("Number 3: ");
            scanf("%d", &userNumber3);
        }
        else
        {
            printf("\nYou don't have enough money for that");
            user_rebet(userBalance, betAmount);
        }
        


        // Generate system's numbers
        systemNumber1 = rand() % 100;
        systemNumber2 = rand() % 100;
        systemNumber3 = rand() % 100;

        printf("System numbers: %d %d %d\n", systemNumber1, systemNumber2, systemNumber3);

        
        int how_many = 5;
        // Calculate the winnings/losses
        int winnings = 0;
        if (userNumber1 == systemNumber1)
        {
            // winnings += betAmount * bet_multiplier;
            how_many++;
        }

        if (userNumber2 == systemNumber2)
        {
            // winnings += betAmount * bet_multiplier;
            how_many++;
        }

        if (userNumber3 == systemNumber3)
        {
            // winnings += betAmount * bet_multiplier;
            how_many++;
        }


        if (how_many < 1)
        {
            winnings = betAmount^how_many;
        }
        else
        {

        // Update user balance
        userBalance += winnings - betAmount;
        }

        printf("how many %d and winnings is %d", how_many, winnings);

        if (winnings > 0) 
        {
            printf("Congratulations! You won ₦%d.\n", winnings);
        } 
        else 
        {
            printf("Sorry, you lost %d.\n", betAmount);
        }

        printf("Play again? (y/n): ");
        scanf(" %c", &playAgain); // Notice the space before %c to consume the newline character from the previous input.

    } while (playAgain == 'y' || playAgain == 'Y' );

    printf("Thank you for playing! Your final balance: %d\n", userBalance);

    return 0;
}
