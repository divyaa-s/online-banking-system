import java.util.HashMap;
import java.util.Map;

public class Bank {
    private Map<String, Map<String, Object>> accounts = new HashMap<>();

    public String createAccount(String id, String name, double initialDeposit) {
        if (accounts.containsKey(id)) {
            return "Account ID already exists!";
        } else {
            Map<String, Object> account = new HashMap<>();
            account.put("name", name);
            account.put("balance", initialDeposit);
            accounts.put(id, account);
            return "Account created successfully!";
        }
    }

    public String displayAccountDetails(String id) {
        if (!accounts.containsKey(id)) {
            return "Account ID does not exist!";
        } else {
            Map<String, Object> account = accounts.get(id);
            return String.format("Account Holder: %s\nAccount Number: %s\nCurrent Balance: %s",
                    account.get("name"), id, account.get("balance"));
        }
    }

    public String depositMoney(String id, double amount) {
        if (!accounts.containsKey(id)) {
            return "Account ID does not exist!";
        }
        if (amount <= 0) {
            return "Invalid deposit amount. Amount must be a positive number.";
        }
        Map<String, Object> account = accounts.get(id);
        double currentBalance = (double) account.get("balance");
        account.put("balance", currentBalance + amount);
        return String.format("Deposited amount: %s\nCurrent balance: %s",
                amount, account.get("balance"));
    }

    public String withdrawMoney(String id, double amount) {
        if (!accounts.containsKey(id)) {
            return "Account ID does not exist!";
        }
        if (amount <= 0) {
            return "Invalid withdrawal amount. Amount must be a positive number.";
        }
        Map<String, Object> account = accounts.get(id);
        double currentBalance = (double) account.get("balance");
        if (amount > currentBalance) {
            return "Insufficient balance!";
        }
        account.put("balance", currentBalance - amount);
        return String.format("Withdrawn amount: %s\nCurrent balance: %s",
                amount, account.get("balance"));
    }

    public Map<String, Map<String, Object>> getAccounts() {
        return accounts;
    }
}
