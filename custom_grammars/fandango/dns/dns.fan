def valid_ns_name(mname, ns_record):
    mname_tokens = mname.split(' ')
    ns_record_tokens = ns_record.split(' ')

    mname_ns = mname_tokens[0]
    ns_record_ns = ns_record_tokens[4]

    if mname_ns == ns_record_ns:
        return True
    else:
        return False


def valid_timeout_conditions(refresh, retry, expire):
    if retry < refresh and expire > refresh + retry:
        return True
    else:
        return False


def valid_glue_record(mname, glue_record):
    mname_tokens = mname.split(' ')
    glue_record_tokens = glue_record.split(' ')

    mname_ns = mname_tokens[0]
    glue_record_ns = glue_record_tokens[0]

    if glue_record_ns == mname_ns:
        return True
    else:
        return False


def unseen_ips(zone):
    zone_lines = zone.split('\n')
    all_ips = []

    for line in zone_lines:
        if line != '':
            tokens = line.split(' ')
            record_type = tokens[3]
            if record_type == 'A' or record_type == 'AAAA':
                all_ips.append(tokens[4])

    unique_ips = set(all_ips)

    if len(unique_ips) == len(all_ips):
        return True
    else:
        return False



<start> ::= <zone>;

<zone> ::= <soa_record> '\n' <ns_record> '\n' <glue_record> '\n' <address_record_list>;

<soa_record> ::= <origin> <ws> <ttl> <ws> 'IN' <ws> 'SOA' <ws> <mname> <ws> <rname> <ws> '(' <ws> <serial> <ws> <refresh> <ws> <retry> <ws> <expire> <ws> <minimum> <ws> ')';

<origin> ::= 'example.com.';

<mname> ::= <ns_label> '.' <origin>;

<ns_label> ::= 'ns' <digit>;

<rname> ::= <mailbox> '.' <origin>;
<mailbox> ::= 'hostmaster' | 'admin' | 'root' | 'postmaster';

<ns_record> ::= <origin> <ws> <ttl> <ws> 'IN' <ws> 'NS' <ws> <ns_label> '.' <origin>;

<glue_record> ::= <ns_label> '.' <origin> <ws> <ttl> <ws> 'IN' <ws> 'A' <ws> <ipv4>;

<address_record_list> ::= <address_record> '\n' <address_record_list>| '';   

<address_record> ::= <origin> <ws> <ttl> <ws> 'IN' <ws> 'A' <ws> <ipv4> | <origin> <ws> <ttl> <ws> 'IN' <ws> 'AAAA' <ws> <ipv6>;

<ws> ::= ' ';

<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';

<ttl> ::= '3600' | '7200' | '14400' | '86400';
<serial> ::= '202' <year> <month> <day> <two_digits>;
<year> ::= '3' | '4' | '5';
<month> ::= '01' | '02' | '03' | '04' | '05' | '06' | '07' | '08' | '09' | '10' | '11' | '12';
<day> ::= '01' | '02' | '03' | '04' | '05' | '06' | '07' | '08' | '09' | '10' | '11' | '12' | '13' | '14' | '15' | '16' | '17' | '18' | '19' | '20' | '21' | '22' | '23' | '24' | '25' | '26' | '27' | '28' | '29' | '30' | '31';
<two_digits> ::= <digit> <digit>;

<refresh> ::= '1200' | '3600' | '7200' | '14400';
<retry>   ::= '180' | '300' | '600' | '900';
<expire>  ::= '604800' | '1209600' | '2419200';
<minimum> ::= '60' | '180' | '300' | '3600';

<ipv4> ::= r"((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\x2e){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])";

<ipv6> ::= r"([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}";

where valid_ns_name(str(<mname>), str(<ns_record>)) and valid_timeout_conditions(int(<refresh>), int(<retry>), int(<expire>)) and unseen_ips(str(<zone>)) and valid_glue_record(str(<mname>), str(<glue_record>))