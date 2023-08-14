#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NUM_LOTTERY_NUMBERS 3

// Function prototypes
void generate_lottery_numbers(int lottery_numbers[]);
void input_user_numbers(int user_numbers[]);
int compare_numbers(const int lottery_numbers[], const int user_numbers[]);
int collect_bet_amount();

int main() {
    int lottery_numbers[NUM_LOTTERY_NUMBERS];
    int user_numbers[NUM_LOTTERY_NUMBERS];
    int betAmount;

    srand(time(NULL));

    generate_lottery_numbers(lottery_numbers);
    input_user_numbers(user_numbers);
    betAmount = collect_bet_amount();


    printf("Lottery Numbers: ");
    for (int i = 0; i < NUM_LOTTERY_NUMBERS; i++) {
        printf("%d ", lottery_numbers[i]);
    }
    printf("\n");

    int matches_power = compare_numbers(lottery_numbers, user_numbers);
    int matches_multiply

    if (matches_power == NUM_LOTTERY_NUMBERS+1) {
        printf("Congratulations! You won the jackpot!\n");
    } else if (matches_power > 0) {
        printf("You matched %d number(s)! Good job!\n", matches_power);
    } else {
        printf("Sorry, you didn't match any numbers. Better luck next time!\n");
    }

    return 0;
}

void generate_lottery_numbers(int lottery_numbers[]) {
    for (int i = 0; i < NUM_LOTTERY_NUMBERS; i++) {
        lottery_numbers[i] = rand() % 10; // Generate random numbers between 0 and 9
    }
}

void input_user_numbers(int user_numbers[]) {
    printf("Enter your lottery numbers (%d numbers between 0 and 9):\n", NUM_LOTTERY_NUMBERS);
    for (int i = 0; i < NUM_LOTTERY_NUMBERS; i++) {
        printf("Number %d: ", i + 1);
        scanf("%d", &user_numbers[i]);
    }
}

int collect_bet_amount() {
    int betAmount;
    printf("Enter your bet amount: ");
    scanf("%d", &betAmount);
    return betAmount;
}

int compare_numbers(const int lottery_numbers[], const int user_numbers[]) {
    int matches_power = 1;// so that reward is not lower than, 
    int matches_multiply = 0;
    
    // raise bet amount by the number of times the input number index is the same as that of the lottery number's index
    for (int i = 0; i < NUM_LOTTERY_NUMBERS; i++) {
        if (lottery_numbers[i] == user_numbers[i]) {
            matches_power+=1;
        }

        // multiply bet amount by the number of times the input number is present in the lottery number
        for (int i = 0; i < NUM_LOTTERY_NUMBERS; i++) {
        for (int j = 0; j < NUM_LOTTERY_NUMBERS; j++) {
            if (lottery_numbers[i] == user_numbers[j]) {
                matches_multiply+=0.6;
            }
        }
    }
    }
    return matches_power, matches_multiply;
}
