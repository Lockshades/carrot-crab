#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

int main() 
{
    int balance = 1000;  // Initial balance
    int bet_amount; // variable for the bet amount
    int user_number; // temporary placeholder for holding the user input
    int game_min = 50, game_max = 1000; // these are the vald betting ranges

    int max_input_range = 9, min_input_range = 0; // ranges for the user input and the game numbers

    int jackpot, normal_win; //wins variables the will be added to the balance once there is a win

    srand(time(0));  // Seed the random number generator with the current time


    printf("Welcome to Balabulu bet! \n");

    while (balance > 0) {
        printf("Your current balance: ₦%d\n", balance);

        printf("Enter your bet amount: ₦");
        scanf("%d", &bet_amount);
        if (bet_amount < game_min || bet_amount > balance || bet_amount>game_max) // input is outside both user
        {
        printf("Invalid bet amount. Please enter a valid bet.\n");
        continue;
        }

        //once bet has been succesfully collected, subtract it from the balance.
        balance-=bet_amount;

        int user_array[3]; // array to stor user input
        int lott_array[3]; // array to store the system lottery numbers

        for (int i = 0; i < 3; i++) // loop to input user number into their respective indexes
        {
            printf(" Enter your-digits %d number (0 to 9): ", i); // print instructions on the constraints
            scanf(" %d", &user_number); // collect the user numbers on each loop run

            if (user_number < 0 || user_number > 9) // make sure that input is neither less than 0 or more than 9
            {
                printf(" Invalid number! Please enter a valid digit for this round again.\n"); // tell the user about the mistake
                i-=1;
                continue; // repeat current loop if arguments are satisfied
            }

            // Generate a random winning number between 0 and 9
            user_array[i] = user_number; // assign the user input for each round into the corresponding index -1.
        }

        max_input_range+=1;
        for (int s = 0; s < 3; s++) // lottery input loop
        {
         lott_array[s] = rand() % max_input_range; // max input range +1 allows system to generate 0 as usual but also generate 9 in this case(29%10=9)
        }

        max_input_range = 9; // reset max_input_range to 9




        // below is better and faster, but rigid(isnt suitable for when the number of lottery digits needs to be changed). I'll fix this later as the time constraint for me is low
        printf(" The lottery numbers are: (%d, %d, %d);\n", lott_array[0], lott_array[1], lott_array[2]);
        printf("Your own guesses are: (%d,%d,%d);\n", user_array[0], user_array[1], user_array[2]);
        
        // Check for winning condition
        float matches_power = 1;
        int matches_multiply = 0; // these variables allow for raising to power when there is a jackpot, and multply when there is no jackpot but also no loss
        for (int i = 0; i < 3; i++) 
        {
            if (lott_array[i] == user_array[i]) // check for jackpot which is when the user input in the same order of the lottery number.
            {
                matches_power += 0.3; // multiply power by 2 for each matching number
            }
            for (int j = 0; j < 3; j++) // simultanuously check the other rows
            {
                if (lott_array[i] == user_array[j]) 
                {
                    matches_multiply+=2; // Increment multiply for each matching number by 2
                }
            }
        }

        if(matches_power>1)// when 2 number are in the same order
        {
            
            jackpot = pow(bet_amount, matches_power);
            printf(" Congratulations on winning the jackpot of ₦%d!\n",jackpot);
            balance+=jackpot;
        }
        else if (matches_power < 1)
        {
            printf(" You didn't win any Jackpot in this round. Better luck next time\n");
            jackpot = 0;
        }

        if (matches_multiply > 0) // meaning the nuber exists but in different order
        {
            normal_win = bet_amount*matches_multiply;
            printf(" You won  ₦%i!\n",normal_win);
            balance+=normal_win;
            
        }
        else
        {
            printf("You lost this round and you lost %d", bet_amount); // reports your loss and how much is lost
        }

        int total = jackpot+normal_win;
        if (total>0)
        {
        printf(" you won %i in total this round so your balance is ₦%d.\n", total, balance);
        }


        int exit = 0; //needs to be initialized in this way so it doesnt auto exit
        printf(" would you like to exit? 0 for NO and 1 for YES.");
        scanf("%d", &exit);
        if (exit==1)
        {
            break; // breaking makes the While loop stop and then your the next line after sadi while loop is run.
        }


        
    }

// beacuase the user might still have balance left of exit, we need to check for the condition and then use printf in consideration for that path
    if(balance>0)
    {
        printf("Thank you for using Balabulu bet! We hope to see back soon\n");
    }
    else
    {
        printf("Game over! You have run out of balance.\n");
        return 0;
    }

    // personal assesments
    // this code has been tested for:
        // *user friendliness - good
        // *arithmetic correctness
        // *only 98% of print statements worked in vscode
        // didnt even work in the online compiler for some reason

        // I consider this done
}
