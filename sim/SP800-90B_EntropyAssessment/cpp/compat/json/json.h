#ifndef RO_TRNG_COMPAT_JSON_JSON_H
#define RO_TRNG_COMPAT_JSON_JSON_H

#include <map>
#include <sstream>
#include <string>
#include <vector>

namespace Json {

class Value {
public:
    enum Kind { Null, Bool, Number, String, Object, Array };

    Value() : kind_(Null), bool_(false), number_(0.0) {}
    Value(const char *value) : kind_(String), bool_(false), number_(0.0), string_(value ? value : "") {}
    Value(const std::string &value) : kind_(String), bool_(false), number_(0.0), string_(value) {}
    Value(double value) : kind_(Number), bool_(false), number_(value) {}
    Value(int value) : kind_(Number), bool_(false), number_(value) {}
    Value(bool value) : kind_(Bool), bool_(value), number_(0.0) {}

    Value &operator=(const char *value) {
        kind_ = String;
        string_ = value ? value : "";
        return *this;
    }
    Value &operator=(const std::string &value) {
        kind_ = String;
        string_ = value;
        return *this;
    }
    Value &operator=(double value) {
        kind_ = Number;
        number_ = value;
        return *this;
    }
    Value &operator=(int value) {
        kind_ = Number;
        number_ = value;
        return *this;
    }
    Value &operator=(bool value) {
        kind_ = Bool;
        bool_ = value;
        return *this;
    }

    Value &operator[](const std::string &key) {
        if (kind_ != Object) {
            kind_ = Object;
            object_.clear();
        }
        return object_[key];
    }

    Value &operator[](const char *key) {
        return (*this)[std::string(key ? key : "")];
    }

    Value &operator[](int index) {
        if (kind_ != Array) {
            kind_ = Array;
            array_.clear();
        }
        if (index < 0) {
            index = 0;
        }
        if (array_.size() <= static_cast<size_t>(index)) {
            array_.resize(static_cast<size_t>(index) + 1);
        }
        return array_[static_cast<size_t>(index)];
    }

    std::string ToString(int indent = 0) const {
        switch (kind_) {
        case Null:
            return "null";
        case Bool:
            return bool_ ? "true" : "false";
        case Number: {
            std::ostringstream out;
            out.precision(17);
            out << number_;
            return out.str();
        }
        case String:
            return "\"" + Escape(string_) + "\"";
        case Array: {
            if (array_.empty()) {
                return "[]";
            }
            std::ostringstream out;
            out << "[\n";
            for (size_t i = 0; i < array_.size(); ++i) {
                out << std::string(indent + 2, ' ') << array_[i].ToString(indent + 2);
                if (i + 1 != array_.size()) {
                    out << ",";
                }
                out << "\n";
            }
            out << std::string(indent, ' ') << "]";
            return out.str();
        }
        case Object: {
            if (object_.empty()) {
                return "{}";
            }
            std::ostringstream out;
            out << "{\n";
            size_t i = 0;
            for (std::map<std::string, Value>::const_iterator it = object_.begin(); it != object_.end(); ++it, ++i) {
                out << std::string(indent + 2, ' ') << "\"" << Escape(it->first) << "\": " << it->second.ToString(indent + 2);
                if (i + 1 != object_.size()) {
                    out << ",";
                }
                out << "\n";
            }
            out << std::string(indent, ' ') << "}";
            return out.str();
        }
        }
        return "null";
    }

private:
    static std::string Escape(const std::string &input) {
        std::ostringstream out;
        for (size_t i = 0; i < input.size(); ++i) {
            const unsigned char c = static_cast<unsigned char>(input[i]);
            switch (c) {
            case '\\': out << "\\\\"; break;
            case '"': out << "\\\""; break;
            case '\b': out << "\\b"; break;
            case '\f': out << "\\f"; break;
            case '\n': out << "\\n"; break;
            case '\r': out << "\\r"; break;
            case '\t': out << "\\t"; break;
            default:
                if (c < 0x20) {
                    out << "\\u";
                    const char *hex = "0123456789abcdef";
                    out << "00" << hex[(c >> 4) & 0xf] << hex[c & 0xf];
                } else {
                    out << input[i];
                }
            }
        }
        return out.str();
    }

    Kind kind_;
    bool bool_;
    double number_;
    std::string string_;
    std::map<std::string, Value> object_;
    std::vector<Value> array_;
};

class StyledWriter {
public:
    std::string write(const Value &value) {
        return value.ToString(0) + "\n";
    }
};

} // namespace Json

#endif
