import hashlib
import os

def generate_hash():
    print("\n" + "="*50)
    print("GENERATE DOCUMENT HASH")
    print("="*50)
    
    # Get user input
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    doc_path = input("Enter document path (or press Enter for test.pdf): ").strip()
    
    # Default to test.pdf if no input
    if not doc_path:
        doc_path = "test.pdf"
    
    # Check if document exists
    if not os.path.exists(doc_path):
        print(f"❌ Error: Document '{doc_path}' not found!")
        return
    
    # Generate hash
    try:
        with open(doc_path, 'rb') as file:
            pdf_data = file.read()
            user_data = (name + age).encode()
            combined_data = pdf_data + user_data
            
            hash_value = hashlib.sha256(combined_data).hexdigest()
        
        # Store with metadata
        with open('main.txt', 'a') as file:
            file.write(f"{name}|{age}|{doc_path}|{hash_value}\n")
        
        print(f"✅ Hash generated successfully!")
        print(f"📄 Document: {doc_path}")
        print(f"👤 User: {name}, Age: {age}")
        print(f"🔐 Hash: {hash_value}")
        print(f"💾 Stored in main.txt")
        
    except Exception as e:
        print(f"❌ Error reading document: {e}")

def verify_document():
    print("\n" + "="*50)
    print("VERIFY DOCUMENT AUTHENTICITY")
    print("="*50)
    
    # Get verification inputs
    name = input("Enter the original name used: ")
    age = input("Enter the original age used: ")
    doc_path = input("Enter document path to verify: ").strip()
    
    if not doc_path:
        doc_path = "test.pdf"
    
    # Check if document exists
    if not os.path.exists(doc_path):
        print(f"❌ Error: Document '{doc_path}' not found!")
        return
    
    try:
        # Generate current hash
        with open(doc_path, 'rb') as file:
            pdf_data = file.read()
            user_data = (name + age).encode()
            combined_data = pdf_data + user_data
            
            current_hash = hashlib.sha256(combined_data).hexdigest()
        
        print(f"🔍 Generated current hash: {current_hash}")
        
        # Search for stored hash
        verification_success = False
        try:
            with open('main.txt', 'r') as file:
                lines = file.readlines()
                
            if not lines:
                print("❌ No hash records found. Generate hashes first.")
                return
            
            print(f"🔎 Searching for matching record...")
            found_match = False
            
            for line_num, line in enumerate(lines, 1):
                parts = line.strip().split('|')
                if len(parts) == 4:
                    stored_name, stored_age, stored_doc, stored_hash = parts
                    
                    if (stored_name == name and stored_age == age and 
                        stored_doc == doc_path):
                        found_match = True
                        print(f"📋 Found stored hash: {stored_hash}")
                        
                        # Compare hashes
                        if stored_hash == current_hash:
                            print("\n" + "✅" * 20)
                            print("✅ DOCUMENT VERIFICATION SUCCESSFUL!")
                            print("✅ Document is AUTHENTIC and UNCHANGED")
                            print("✅" * 20)
                            verification_success = True
                        else:
                            print("\n" + "❌" * 20)
                            print("❌ DOCUMENT VERIFICATION FAILED!")
                            print("❌ Document may have been TAMPERED with")
                            print("❌" * 20)
                            print(f"🔍 Hash comparison:")
                            print(f"   Stored:  {stored_hash}")
                            print(f"   Current: {current_hash}")
                        break
            
            if not found_match:
                print(f"❌ No matching record found for:")
                print(f"   Name: {name}, Age: {age}, Document: {doc_path}")
                
        except FileNotFoundError:
            print("❌ No hash records found. Generate hashes first.")
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")

def view_stored_hashes():
    print("\n" + "="*50)
    print("STORED HASH RECORDS")
    print("="*50)
    
    try:
        with open('main.txt', 'r') as file:
            lines = file.readlines()
        
        if not lines:
            print("No hash records found.")
            return
        
        for i, line in enumerate(lines, 1):
            parts = line.strip().split('|')
            if len(parts) == 4:
                name, age, doc, hash_val = parts
                print(f"{i}. 👤 {name} ({age}) | 📄 {doc}")
                print(f"   🔐 {hash_val}")
                print("   " + "-" * 40)
            else:
                print(f"{i}. Invalid format: {line}")
                
    except FileNotFoundError:
        print("No hash records found.")

def main_menu():
    while True:
        print("\n" + "="*50)
        print("🔐 DOCUMENT VERIFICATION SYSTEM")
        print("="*50)
        print("1. 📄 Generate Document Hash")
        print("2. 🔍 Verify Document Authenticity") 
        print("3. 📋 View Stored Hashes")
        print("4. 🚪 Exit")
        print("="*50)
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == '1':
            generate_hash()
        elif choice == '2':
            verify_document()
        elif choice == '3':
            view_stored_hashes()
        elif choice == '4':
            print("👋 Thank you for using the Document Verification System!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

# Run the program
if __name__ == "__main__":
    main_menu()