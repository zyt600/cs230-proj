<start> ::= <zone>;

<zone> ::= <zone_core>;

<zone_core> ::= <soa_record> '\n' <ns_record> '\n' <resource_records> ; 

<ns_record> ::= '\tNS\t' <domain_name>;

<soa_record> ::= <rname> '\t' 'SOA' '\t';

<resource_records> ::= <resource_record> '\n' <resource_records> | <resource_record>;

<resource_record> ::= <record>;

<record> ::= <rname> '\t' <rtype> '\t' <rdata>;

<rname> ::= <domain_name>;

<rtype> ::= 'A' | 'AAAA' ;

<rdata> ::= <ip_address> | <aaaa_address>;

<domain_name> ::= <labels>;

<labels> ::= <label> '.' <label> | <labels> '.' <label> ;

<label> ::= <char_string>;

<char_string> ::= <char> | <char> <char> | <char> <char> <char> ;

<aaaa_address> ::= <ip6_part> | <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part>;


<ip_address> ::= <digit> '.' <digit> '.' <digit> '.' <digit>;

<digit> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';

<char> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' ;

<ip6_part> ::= <hex_digit> | <hex_digit> <hex_digit> | <hex_digit> <hex_digit> <hex_digit> | <hex_digit> <hex_digit> <hex_digit> <hex_digit> ;

<hex_digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' ;




