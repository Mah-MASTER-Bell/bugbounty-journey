
import requests
import csv

# 1. Create a list of 10 parameters
parameters = ['id', 'user', 'name', 'pass', 'email', 'phone', 'address', 'city', 'country', 'zip']

# 2. Setup CSV file to save the results
with open('fuzz_results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Parameter', 'Status Code', 'Response Length'])

    # 3. Loop through the parameters
    for parameter_name in parameters:
        url = f"https://httpbin.org/get?{parameter_name}=test"

        # 4. Use try/except for error handling
        try:
            response = requests.get(url)
            status = response.status_code
            length = len(response.text)

            # Print to terminal
            print(f"Parameter: {parameter_name} | Status: {status} | Length: {length}")

            # Save to CSV
            writer.writerow([parameter_name, status, length])

        except requests.exceptions.RequestException as e:
            print(f"Error with parameter {parameter_name}: {e}")
            writer.writerow([parameter_name, "ERROR", "ERROR"])

print("\nDone! Results saved to fuzz_results.csv")

