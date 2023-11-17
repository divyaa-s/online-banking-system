import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;
import java.util.Scanner;



public class CustomerRegistrationConsole {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Customer Registration");

        System.out.print("Type (Savings/Current): ");
        String type = scanner.nextLine();

        System.out.print("Name: ");
        String name = scanner.nextLine();

        System.out.print("D.O.B: ");
        String dob = scanner.nextLine();

        System.out.print("Address: ");
        String address = scanner.nextLine();

        System.out.print("Email: ");
        String email = scanner.nextLine();

        System.out.print("Phone: ");
        String phone = scanner.nextLine();

        System.out.print("Password: ");
        String password = scanner.nextLine();

        System.out.print("Confirm Password: ");
        String confirmPassword = scanner.nextLine();

        System.out.print("Initial Balance: ");
        double initialBalance = scanner.nextDouble();

        handleSubmit(type, name, dob, address, email, phone, password, confirmPassword, initialBalance);
        scanner.close();
    }

    private static void handleSubmit(String type, String name, String dob, String address, String email,
                                     String phone, String password, String confirmPassword, double initialBalance) {
        if (type.isEmpty() || name.isEmpty() || dob.isEmpty() || address.isEmpty() || email.isEmpty() ||
                phone.isEmpty() || password.isEmpty() || confirmPassword.isEmpty()) {
            System.out.println("Error: All fields are required.");
            return;
        }

        if (!password.equals(confirmPassword)) {
            System.out.println("Error: Passwords do not match.");
            return;
        }

        if (phone.length() != 10 || !phone.matches("\\d{10}")) {
            System.out.println("Error: Phone number must be numeric and contain exactly 10 digits.");
            return;
        }

        if (!isValidEmail(email)) {
            System.out.println("Error: Invalid email address.");
            return;
        }

        String accountNumber = generateAccountNumber();

        System.out.println("Success: Data saved successfully.");

        try (FileWriter writer = new FileWriter("customers.csv", true)) {
            writer.append(accountNumber).append(",")
                    .append(type).append(",")
                    .append(name).append(",")
                    .append(dob).append(",")
                    .append(address).append(",")
                    .append(email).append(",")
                    .append(phone).append(",")
                    .append(password).append(",")
                    .append(String.valueOf(initialBalance)).append("\n");
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    private static String generateAccountNumber() {
        Random random = new Random();
        StringBuilder accountNumber = new StringBuilder();
        for (int i = 0; i < 10; i++) {
            accountNumber.append(random.nextInt(10));
        }
        return accountNumber.toString();
    }

    private static boolean isValidEmail(String email) {
        String emailRegex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$";
        return email.matches(emailRegex);
    }
}

