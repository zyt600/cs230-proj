<start> ::= <zone>;

<zone> ::= <soa_record> <ns_record> <glue_record> <address_record_list>;

<soa_record> ::= <origin> <ws> <ttl> <ws> 'IN' <ws> 'SOA' <ws> <mname> <ws> <rname> <ws> '(' <ws> <serial> <ws> <refresh> <ws> <retry> <ws> <expire> <ws> <minimum> <ws> ')';

<origin> ::= 'example.com.';

<mname> ::= <ns_label> '.' <origin>;
<ns_label> ::= 'ns' <digit>;

<rname> ::= <mailbox> '.' <origin>;
<mailbox> ::= 'hostmaster' | 'admin' | 'root' | 'postmaster';

<ns_record> ::= <origin> <ws> <ttl> <ws> 'IN' <ws> 'NS' <ws> <ns_label> '.' <origin>;

<glue_record> ::= <ns_label> '.' <origin> <ws> <ttl> <ws> 'IN' <ws> 'A' <ws> <ipv4>;

<address_record_list> ::= <address_record> <address_record_list>| '';   

<address_record> ::= <origin> <ws> <ttl> <ws> 'IN' <ws> 'A' <ws> <ipv4> | <origin> <ws> <ttl> <ws> 'IN' <ws> 'AAAA' <ws> <ipv6>;

<ws> ::= ' ' | '\t';

<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';

<ttl> ::= '3600' | '7200' | '14400' | '86400';
<serial> ::= '20230101' | '20230201' | '20230301' | '20230401';
<refresh> ::= '1200' | '3600' | '7200' | '14400';
<retry>   ::= '180' | '300' | '600' | '900';
<expire>  ::= '604800' | '1209600' | '2419200';
<minimum> ::= '60' | '180' | '300' | '3600';

<ipv4> ::= <digit> '.' <digit> '.' <digit> '.' <digit>;

<hex_digit> ::= '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'|'a'|'b'|'c'|'d'|'e'|'f';

<ip6_part> ::= <hex_digit> | <hex_digit> <hex_digit> | <hex_digit> <hex_digit> <hex_digit> | <hex_digit> <hex_digit> <hex_digit> <hex_digit>;

<ipv6> ::= <ip6_part> | <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> | <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part> ':' <ip6_part>;

