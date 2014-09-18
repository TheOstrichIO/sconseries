// Copyright 2014 The Ostrich

#include <iostream>  // NOLINT(readability/streams)
#include <string>

#include "AddressBook/addressbook.h"

using std::cout;
using std::cin;
using std::getline;
using std::string;

// This function fills in a Person object based on user input.
void PromptForAddress(Person* person) {
    cout << "Enter person ID number: ";
    int id;
    cin >> id;
    person->set_id(id);
    cin.ignore(256, '\n');

    cout << "Enter name: ";
    string name;
    getline(cin, name);
    person->set_name(name);

    cout << "Enter email address (blank for none): ";
    string email;
    getline(cin, email);
    person->set_email(email);

    cout << "Enter a phone number (or leave blank to finish): ";
    string number;
    getline(cin, number);
    if (!number.empty()) {
        person->phone.set_number(number);
        cout << "Is this a mobile, home, or work phone? ";
        string type;
        getline(cin, type);
        if (type == "mobile") {
            person->phone.set_type(PhoneNumber::MOBILE);
        } else if (type == "home") {
            person->phone.set_type(PhoneNumber::HOME);
        } else if (type == "work") {
            person->phone.set_type(PhoneNumber::WORK);
        } else {
            cout << "Unknown phone type.  Using UNSPECIFIED.\n";
            person->phone.set_type(PhoneNumber::UNSPECIFIED);
        }
    }
}

// Main function:  Reads the entire address book from a file,
//   adds one person based on user input, then writes it back out to the same
//   file.
int main(int argc, char* argv[]) {
    Person person;

    // Get an address.
    PromptForAddress(&person);

    cout << "Got: " << person.name() << "\n";

    return 0;
}

