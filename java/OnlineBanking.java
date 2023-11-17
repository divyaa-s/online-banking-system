import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class OnlineBanking {
    private Map<String, Map<String, String>> accounts = new HashMap<>();

    public static void main(String[] args) {
        OnlineBanking onlineBanking = new OnlineBanking();
        onlineBanking.loadFromCSV();

        Scanner scanner = new Scanner(System.in);
        int choice;

        do {
            System.out.println("1. Display Account Details");
            System.out.println("2. Deposit Money");
            System.out.println("3. Withdraw Money");
            System.out.println("4. Modify Account Details");
            System.out.println("5. Exit");
            System.out.print("Enter your choice: ");
            choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    onlineBanking.displayAccountDetails();
                    break;
                case 2:
                    onlineBanking.depositMoney();
                    break;
                case 3:
                    onlineBanking.withdrawMoney();
                    break;
                case 4:
                    onlineBanking.modifyDetails();
                    break;
                case 5:
                    System.out.println("Exiting the program. Goodbye!");
                    break;
                default:
                    System.out.println("Invalid choice. Please enter a valid option.");
            }

        } while (choice != 5);

        scanner.close();
    }

    private void loadFromCSV() {
        String line;
        try (BufferedReader br = new BufferedReader(new FileReader("customers.csv"))) {
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",");
                Map<String, String> accountDetails = new HashMap<>();
                accountDetails.put("accountType", parts[1]);
                accountDetails.put("name", parts[2]);
                accountDetails.put("dob", parts[3]);
                accountDetails.put("address", parts[4]);
                accountDetails.put("email", parts[5]);
                accountDetails.put("phoneNumber", parts[6]);
                accountDetails.put("password", parts[7]);
                accountDetails.put("balance", parts[8]);

                accounts.put(parts[0], accountDetails);
            }
        } catch (IOException e) {
            System.err.println("Error reading from customers.csv: " + e.getMessage());
        }
    }

    private void displayAccountDetails() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter Account Number: ");
        String accountNumber = scanner.next();
        scanner.close();

        Map<String, String> account = accounts.get(accountNumber);
        if (account != null) {
            System.out.println("Account Holder: " + account.get("name"));
            System.out.println("Account Number: " + accountNumber);
            System.out.println("Account Type: " + account.get("accountType"));
            System.out.println("Current Balance: " + account.get("balance"));
        } else {
            System.out.println("Account Number does not exist!");
        }
    }

    private void depositMoney() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter Account Number: ");
        String accountNumber = scanner.next();
        Map<String, String> account = accounts.get(accountNumber);
        if (account != null) {
            System.out.print("Enter Deposit Amount: ");
            double depositAmount = scanner.nextDouble();
            double currentBalance = Double.parseDouble(account.get("balance"));
            currentBalance += depositAmount;
            account.put("balance", String.valueOf(currentBalance));
            System.out.println("Deposited amount: " + depositAmount);
            System.out.println("Current balance: " + currentBalance);
        } else {
            System.out.println("Account Number does not exist!");
        }
        scanner.close();
    }

    private void withdrawMoney() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter Account Number: ");
        String accountNumber = scanner.next();
        Map<String, String> account = accounts.get(accountNumber);
        if (account != null) {
            System.out.print("Enter Withdrawal Amount: ");
            double withdrawalAmount = scanner.nextDouble();
            double currentBalance = Double.parseDouble(account.get("balance"));
            if (withdrawalAmount <= currentBalance) {
                currentBalance -= withdrawalAmount;
                account.put("balance", String.valueOf(currentBalance));
                System.out.println("Withdrawn amount: " + withdrawalAmount);
                System.out.println("Current balance: " + currentBalance);
            } else {
                System.out.println("Insufficient balance!");
            }
        } else {
            System.out.println("Account Number does not exist!");
        }
        scanner.close();

    }

    private void modifyDetails() {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter Account Number: ");
        String accountNumber = scanner.next();
        Map<String, String> account = accounts.get(accountNumber);
        if (account != null) {
            System.out.print("Enter new phone number: ");
            String newPhoneNumber = scanner.next();
            System.out.print("Enter new email address: ");
            String newEmail = scanner.next();

            account.put("phone_number", newPhoneNumber);
            account.put("email", newEmail);
            System.out.println("Phone number and email updated successfully.");

            // Update the existing data in the customers.csv file
            updateCustomersCSV(accountNumber, newPhoneNumber, newEmail);
        } else {
            System.out.println("Account Number does not exist!");
        }
        scanner.close();
    }

    private void updateCustomersCSV(String accountNumber, String newPhoneNumber, String newEmail) {
        try {
            File inputFile = new File("customers.csv");
            File tempFile = new File("temp_customers.csv");

            BufferedReader reader = new BufferedReader(new FileReader(inputFile));
            BufferedWriter writer = new BufferedWriter(new FileWriter(tempFile));

            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                String csvAccountNumber = parts[0].trim();
                if (csvAccountNumber.equals(accountNumber)) {
                    // Update the line with new phone number and email
                    parts[6] = newPhoneNumber;
                    parts[5] = newEmail;
                }
                writer.write(String.join(",", parts) + "\n");
            }

            writer.close();
            reader.close();

            // Rename the temp file to the original file
            if (tempFile.renameTo(inputFile)) {
                System.out.println("Data updated in customers.csv");
            } else {
                System.out.println("Error updating data in customers.csv");
            }
        } catch (IOException e) {
            System.err.println("Error updating data in customers.csv: " + e.getMessage());
        }
    }
}