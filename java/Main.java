import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Map;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Bank bank = new Bank();        Map<String, String> adminCredentials = AdminCredentialsChecker.readAdminCredentials();
        boolean exitFlag = false;

        // Create a single Scanner for user input
        try (Scanner scanner = new Scanner(System.in)) {
            while (!exitFlag) {
                System.out.println("\n1. Admin\n2. Customer\n3. Exit");

                String choice = scanner.nextLine();

                switch (choice) {
                    case "1":
                        adminOptions(bank, adminCredentials, scanner);
                        break;
                    case "2":
                        customerOptions(bank, adminCredentials, scanner);
                        break;
                    case "3":
                        exitFlag = true;
                        System.out.println("Exiting the application.");
                        break;
                    default:
                        System.out.println("Invalid choice. Please enter a valid option.");
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void adminOptions(Bank bank, Map<String, String> adminCredentials, Scanner scanner) {
        System.out.print("Enter admin username: ");
        String username = scanner.nextLine();
        System.out.print("Enter admin password: ");
        String password = scanner.nextLine();

        if (adminCredentials.containsKey(username) && adminCredentials.get(username).equals(password)) {
            System.out.println("Admin login successful!");
            adminMenu(bank, adminCredentials, scanner);
        } else {
            System.out.println("Invalid admin credentials. Please try again.");
        }
    }


    private static void adminMenu(Bank bank, Map<String, String> adminCredentials, Scanner scanner) {
        while (true) {
            System.out.println("\nAdmin Menu\n1. Add Admin\n2. Search Customer Account\n3. Delete Customer Account\n4. Exit");
            String choice = scanner.nextLine();

            switch (choice) {
                case "1":
                    addAdmin(adminCredentials, scanner);
                    break;
                case "2":
                    searchAccount(bank, scanner);
                    break;
                case "3":
                    deleteAccount(bank, scanner);
                    break;
                case "4":
                    System.out.println("Returning to the main menu.");
                    return;
                default:
                    System.out.println("Invalid choice. Please enter a valid option.");
            }
        }
    }

    private static void addAdmin(Map<String, String> adminCredentials, Scanner scanner) {
        System.out.print("Enter new admin username: ");
        String newUsername = scanner.nextLine();
        System.out.print("Enter new admin password: ");
        String newPassword = scanner.nextLine();

        adminCredentials.put(newUsername, newPassword);
        AdminCredentialsChecker.writeAdminCredentials(adminCredentials);

        System.out.println("Admin added successfully!");
    }

    private static void searchAccount(Bank bank, Scanner scanner) {
        try {
            System.out.print("Enter account number to search: ");
            String accountNumberToSearch = scanner.nextLine();
    
            Map<String, Map<String, Object>> accounts = bank.getAccounts();
            if (accounts.containsKey(accountNumberToSearch)) {
                Map<String, Object> account = accounts.get(accountNumberToSearch);
                System.out.println(String.format("Account found!\nAccount Holder: %s\nAccount Balance: %s",
                        account.get("name"), account.get("balance")));
            } else if (searchAccountInCSV(accountNumberToSearch)) {
                System.out.println("Account found in temp_customers.csv!");
            } else {
                System.out.println("Account not found!");
            }
        } catch (Exception e) {
            System.out.println("An error occurred while searching for the account.");
            e.printStackTrace();
        }
    }
    

private static boolean searchAccountInCSV(String accountNumber) {
    try (BufferedReader reader = new BufferedReader(new FileReader("temp_customers.csv"))) {
        String line;
        while ((line = reader.readLine()) != null) {
            String[] parts = line.split(",");
            String csvAccountNumber = parts[0].trim();
            if (csvAccountNumber.equals(accountNumber)) {
                // Account found in CSV, display details or return as needed
                System.out.println("Details from temp_customers.csv:");
                System.out.println("Account Holder: " + parts[2].trim());
                System.out.println("Balance: " + parts[8].trim());
                return true;
            }
        }
    } catch (IOException e) {
        System.out.println("An error occurred while reading temp_customers.csv.");
        e.printStackTrace();
    }
    return false;
}
    

private static void deleteAccount(Bank bank, Scanner scanner) {
    try {
        System.out.print("Enter account number to delete: ");
        String accountNumberToDelete = scanner.nextLine();

        Map<String, Map<String, Object>> accounts = bank.getAccounts();
        if (accounts.containsKey(accountNumberToDelete)) {
            // Delete the account from the map
            accounts.remove(accountNumberToDelete);

            // Update the customers.csv file
            writeCustomerData(accounts);

            System.out.println("Account deleted successfully!");
        } else {
            System.out.println("Account not found in memory, checking temp_customers.csv...");

            // Check the customers.csv file
            if (deleteAccountInCSV(accountNumberToDelete)) {
                System.out.println("Account deleted from temp_customers.csv!");
            } else {
                System.out.println("Account not found!");
            }
        }
    } catch (Exception e) {
        System.out.println("An error occurred while deleting the account.");
        e.printStackTrace();
    }
}

private static boolean deleteAccountInCSV(String accountNumber) {
    try (BufferedReader reader = new BufferedReader(new FileReader("temp_customers.csv"))) {
        StringBuilder newCsvContent = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            String[] parts = line.split(",");
            String csvAccountNumber = parts[0].trim();
            if (!csvAccountNumber.equals(accountNumber)) {
                // Keep the account in the new content
                newCsvContent.append(line).append("\n");
            }
        }

        // Update the customers.csv file with the new content
        try (FileWriter writer = new FileWriter("temp_customers.csv")) {
            writer.write(newCsvContent.toString());
            return true;
        }
    } catch (IOException e) {
        System.out.println("An error occurred while reading or writing customers.csv.");
        e.printStackTrace();
    }
    return false;
}


private static void customerOptions(Bank bank, Map<String, String> adminCredentials, Scanner scanner) {
    while (true) {
        System.out.println("\n1. Login\n2. Register\n3. Back to main menu");

        String choice = scanner.nextLine();

        switch (choice) {
            case "1":
    System.out.print("Enter account number: ");
    String accId = scanner.nextLine();
    System.out.print("Enter account password: ");
    String password = scanner.nextLine();

    if (bank.getAccounts().containsKey(accId)) {
        Map<String, Object> account = bank.getAccounts().get(accId);

        // Ensure that the keys match the actual keys in your CSV data
        String storedPassword = (String) account.get("Password"); // Update the key to match your CSV
        String storedAccountType = (String) account.get("Account Type"); // Update the key to match your CSV

        if (password.equals(storedPassword) && "savings".equalsIgnoreCase(storedAccountType)) {
            System.out.println("Customer login successful!");
            // You can add customer functionalities here
        } else {
            System.out.println("Invalid account number, password, or account type.");
        }
    } else {
        System.out.println("Invalid account number.");
    }
    break;


            case "2":
                // You can add the customer registration process here
                System.out.println("Customer registration process");
                break;
            case "3":
                System.out.println("Returning to the main menu.");
                return;
            default:
                System.out.println("Invalid choice. Please enter a valid option.");
        }
    }
}

    

    private static void writeCustomerData(Map<String, Map<String, Object>> accounts) {
        try (FileWriter writer = new FileWriter("temp_customers.csv")) {
            for (Map.Entry<String, Map<String, Object>> entry : accounts.entrySet()) {
                String id = entry.getKey();
                Map<String, Object> account = entry.getValue();
                writer.write(id + "," + account.get("name") + "," + account.get("balance") + "\n");
            }
        } catch (IOException e) {
            System.out.println("An error occurred while writing customer data to the file.");
            e.printStackTrace();
        }
    }
}
