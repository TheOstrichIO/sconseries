// Copyright 2014 The Ostrich
// AddressBook data structures logic
// Author: ItamarO

#include <string>

#include "AddressBook/addressbook.h"

std::string PhoneNumber::number() const {
    return number_;
}

void PhoneNumber::set_number(const std::string& number) {
    number_ = number;
}

PhoneNumber::PhoneType PhoneNumber::type() const {
    return type_;
}

void PhoneNumber::set_type(PhoneType type) {
    type_ = type;
}

std::string Person::name() const {
    return name_;
}

void Person::set_name(const std::string& name) {
    name_ = name;
}

std::string Person::email() const {
    return email_;
}

void Person::set_email(const std::string& email) {
    email_ = email;
}

int Person::id() const {
    return id_;
}

void Person::set_id(int id) {
    id_ = id;
}
