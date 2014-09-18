// Copyright 2014 The Ostrich
// AddressBook data structures
// Author: ItamarO

#ifndef ADDRESSBOOK_ADDRESSBOOK_H_
#define ADDRESSBOOK_ADDRESSBOOK_H_

#include <string>

class PhoneNumber {
 public:
    enum PhoneType {
        UNSPECIFIED = 0,
        MOBILE,
        HOME,
        WORK
    };
    std::string number() const;
    void set_number(const std::string& number);
    PhoneType type() const;
    void set_type(PhoneType type);

 private:
    std::string number_;
    PhoneType type_;
};

class Person {
 public:
    std::string name() const;
    void set_name(const std::string& name);
    int id() const;
    void set_id(int id);
    std::string email() const;
    void set_email(const std::string& email);
    PhoneNumber phone;

 private:
    std::string name_;
    int id_;
    std::string email_;
};

#endif  // ADDRESSBOOK_ADDRESSBOOK_H_
