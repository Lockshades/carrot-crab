#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUM_LOTTERY_NUMBERS 3

// Function prototypes
void generate_lottery_numbers(int lottery_numbers[]);
void input_user_numbers(int user_numbers[]);
int collect_bet_amount();

int main() 
{
    
    int continuePlaying; 

    
        int lottery_numbers[NUM_LOTTERY_NUMBERS];
        int user_numbers[NUM_LOTTERY_NUMBERS];
        int betAmount;

        int matches_power = 1; // Start with a base power of 1
        int matches_multiply = 0;

    int balance = 10000;
    printf("Your balance: ₦%d\n", balance);

    while (continuePlaying) 
    {   
        

        srand(time(NULL));

        
        generate_lottery_numbers(lottery_numbers);
        input_user_numbers(user_numbers);
        betAmount = collect_bet_amount();
        balance-=betAmount;
        printf("your balance: %d", balance);

        printf("\nLottery Numbers: ");
        for (int i = 0; i < NUM_LOTTERY_NUMBERS; i++) 
        {
            printf("%d ", lottery_numbers[i]);
        }
        printf("\n");

        

        for (int i = 0; i < NUM_LOTTERY_NUMBERS; i++) 
        {
            if (lottery_numbers[i] == user_numbers[i]) 
            {
                matches_power += 0.5; // Increase power by 0.5 for each matching number(max 2.5 in total)
            }
            for (int j = 0; j < NUM_LOTTERY_NUMBERS; j++) {
                if (lottery_numbers[i] == user_numbers[j]) 
                {
                    matches_multiply+=2; // Increment multiply for each matching number by 2
                }
            }
        }

        return balance;
    }

    int jackpot = (betAmount ^ matches_multiply);
    int simple_win = (betAmount*matches_power);
    printf("\nbetAmount: %d", betAmount);

    if (matches_power > 1) 
    {
        printf("\nCongratulations on winning the jackpot!\n You won %d.\n\n", jackpot);
    }

    if (matches_multiply > 0) 
    {
        printf("\nYou matched %d number(s) with a multiplier of %d! Your total win: %d\n\n", matches_multiply/2, matches_multiply, simple_win);
    } else {
        printf("\nSorry, you didn't match any numbers. Better luck next time!\n");
    }


    // calculate and print balance
    if (matches_multiply>0)
    {
        balance += jackpot + simple_win;
        printf("Your new balance: ₦%d", balance);
    }


    printf("\nDo you want to play another round? (1 for Yes, 0 for No): ");
    scanf(" %d", &continuePlaying);

    printf("Thank you for playing!\n");


    return 0;
}

void generate_lottery_numbers(int lottery_numbers[]) 
{
    for (int i = 0; i < NUM_LOTTERY_NUMBERS; i++) 
    {
        lottery_numbers[i] = rand() % 10; // Generate random numbers between 0 and 9
    }
}

void input_user_numbers(int user_numbers[]) 
{
    printf("Enter your lottery numbers (%d numbers between 0 and 9):\n", NUM_LOTTERY_NUMBERS);
    for (int i = 0; i < NUM_LOTTERY_NUMBERS; i++) 
    {
        printf("Number %d: ", i + 1);
        scanf("%d", &user_numbers[i]);
    }
}

int collect_bet_amount() 
{
    int betAmount;
    printf("Enter your bet amount: ");
    scanf("%d", &betAmount);
    return betAmount;
}
