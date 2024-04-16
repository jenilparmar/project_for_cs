import csv

def read_users_from_csv(file_path):
    users = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row)
    return users

def write_user_to_csv(user, file_path):
    fieldnames = ["username", "email", "password"]  # Define field names
    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:  # Check if file is empty
            writer.writeheader()  # Write header if file is empty
        writer.writerow(user)

# Example usage:
user = {"username": "Jenil_2", "email": "jenilparmar_2@gmail.com", "password": "Sharam_nahi_ati_PassWard_dekhneme?"}
write_user_to_csv(user, "users.csv")
