#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int balance = 1000;  // Initial balance
    int bet_amount;
    int user_number, winning_number;

    srand(time(0));  // Seed the random number generator with the current time

    while (balance > 0) {
        printf("Your current balance: %d\n", balance);

        printf("Enter your bet amount: ");
        scanf("%d", &bet_amount);

        if (bet_amount <= 0 || bet_amount > balance) {
            printf("Invalid bet amount. Please enter a valid bet.\n");
            continue;
        }

        printf("Enter your 3-digit number (000 to 999): ");
        scanf("%d", &user_number);

        if (user_number < 0 || user_number > 999) {
            printf("Invalid number. Please enter a valid 3-digit number.\n");
            continue;
        }

        // Generate a random winning number between 0 and 999
        winning_number = rand() % 1000;
        printf("Winning number: %03d\n", winning_number);

        // Extract individual digits from user and winning numbers
        int user_digit1 = user_number / 100;
        int user_digit2 = (user_number / 10) % 10;
        int user_digit3 = user_number % 10;

        int winning_digit1 = winning_number / 100;
        int winning_digit2 = (winning_number / 10) % 10;
        int winning_digit3 = winning_number % 10;

        // Check for winning condition
        if (user_number == winning_number) {
            printf("Congratulations! You won!\n");
            balance += bet_amount * 1000;  // Win 1000 times the bet amount
        } else if (user_digit1 == winning_digit1 || user_digit2 == winning_digit2 || user_digit3 == winning_digit3) {
            printf("Partial match! You get back half of your bet.\n");
            balance += bet_amount / 2;  // Win back half of the bet amount
        } else {
            printf("Sorry, you lost.\n");
            balance -= bet_amount;  // Lose the bet amount
        }
    }

    printf("Game over! You have run out of balance.\n");
    return 0;
}
