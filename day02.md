
# Day 2 - DNS Records, Reconnaissance, and Automation

## 1. DNS Record Types
- **A Record:** Maps a domain name to IPv4 (32 bits / 4 bytes). Finds the server's IPv4 address.
- **AAAA Record:** Maps a domain name to IPv6 (128 bits / 16 bytes). Finds the server's IPv6 address.
- **CNAME Record:** Creates an alternative (alias) name for a targeted domain. Example: `www.example.com` points to `example.com`. It is necessary because it creates aliases for domains, not for IP addresses.
- **MX Record:** Mail Exchange. Specific for mail servers and receiving emails for a domain. MX records tell email where to go, and the MX record itself needs an IP to reach the servers.
- **TXT Record:** Contains arbitrary text data associated with a specific domain. Used for verification and security, such as Google/Microsoft site ownership verification, and SPF/DKIM records to prevent spoofing.

## 2. Kali Linux Tools
- **DIG (Domain Information Groper):** A command-line tool that gives information on DNS records. You can check how many mail servers there are (MX), IPv4 (A), IPv6 (AAAA), and `+trace` to see the authoritative DNS record from the root.
- **dnsrecon:** `-d` stands for domain, `-t std` stands for standard scan. Command used: `dnsrecon -d tesla.com -t std`.
- **amass:** A reconnaissance tool used to map the attack surface. `enum` means enumeration (listing down related things, just like finding subdomains). `-passive` uses publicly available resources for collecting info without directly touching the target's servers.

## 3. Why Subdomains Expand the Bug Bounty Attack Surface
Subdomains expand the attack surface area. Every subdomain holds a different type of service (e.g., VPN, mail, API). If any subdomain runs on outdated software, it can cause known vulnerabilities. Subdomains may have weaker security controls. If a subdomain is forgotten, it may cause misconfigurations. Different subdomains are often handled by different security practices or development teams.

---

## 4. Kali Linux Raw Terminal Output

### A. `dig` (Root Server Query)
```text
; <<>> DiG 9.20.11-4+b1-Debian <<>>
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 27929
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 13, AUTHORITY: 0, ADDITIONAL: 27

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1220
; COOKIE: f37a3c21f365c572010000006ad7d94c5a0f84538bb8572b (good)
;; QUESTION SECTION:
;.                              IN      NS

;; ANSWER SECTION:
.                       80722   IN      NS      c.root-servers.net.
.                       80722   IN      NS      b.root-servers.net.
.                       80722   IN      NS      i.root-servers.net.
.                       80722   IN      NS      j.root-servers.net.
.                       80722   IN      NS      k.root-servers.net.
.                       80722   IN      NS      d.root-servers.net.
.                       80722   IN      NS      m.root-servers.net.
.                       80722   IN      NS      h.root-servers.net.
.                       80722   IN      NS      f.root-servers.net.
.                       80722   IN      NS      a.root-servers.net.
.                       80722   IN      NS      e.root-servers.net.
.                       80722   IN      NS      l.root-servers.net.
.                       80722   IN      NS      g.root-servers.net.

;; ADDITIONAL SECTION:
a.root-servers.net.     253510  IN      A       198.41.0.4
b.root-servers.net.     604276  IN      A       170.247.170.2
c.root-servers.net.     604473  IN      A       192.33.4.12
d.root-servers.net.     604473  IN      A       199.7.91.13
e.root-servers.net.     512238  IN      A       192.203.230.10
f.root-servers.net.     253814  IN      A       192.5.5.241
g.root-servers.net.     504921  IN      A       192.112.36.4
h.root-servers.net.     512238  IN      A       198.97.190.53
i.root-servers.net.     157199  IN      A       192.36.148.17
j.root-servers.net.     604474  IN      A       192.58.128.30
k.root-servers.net.     598987  IN      A       193.0.14.129
l.root-servers.net.     428189  IN      A       199.7.83.42
m.root-servers.net.     511074  IN      A       202.12.27.33
a.root-servers.net.     118121  IN      AAAA    2001:503:ba3e::2:30
b.root-servers.net.     517973  IN      AAAA    2801:1b8:10::b
c.root-servers.net.     157199  IN      AAAA    2001:500:2::c
d.root-servers.net.     157199  IN      AAAA    2001:500:2d::d
e.root-servers.net.     157199  IN      AAAA    2001:500:a8::e
f.root-servers.net.     591910  IN      AAAA    2001:500:2f::f
g.root-servers.net.     157199  IN      AAAA    2001:500:12::d0d
h.root-servers.net.     157199  IN      AAAA    2001:500:1::53
i.root-servers.net.     157199  IN      AAAA    2001:7fe::53
j.root-servers.net.     157199  IN      AAAA    2001:503:c27::2:30
k.root-servers.net.     601475  IN      AAAA    2001:7fd::1
l.root-servers.net.     157199  IN      AAAA    2001:500:9f::42
m.root-servers.net.     604120  IN      AAAA    2001:dc3::35

;; Query time: 12 msec
;; SERVER: 192.168.1.1#53(192.168.1.1) (UDP)
;; WHEN: Tue Oct 20 17:12:42 EDT 2026
;; MSG SIZE  rcvd: 851
```

### B. `dig +trace google.com` (The DNS Chain)
*Annotation:* The output below shows the resolver starting at the Root servers (`.`), getting the `.com` TLD servers, then getting Google's Authoritative nameservers, and finally resolving the IP `142.251.37.142`.

```text
; <<>> DiG 9.20.11-4+b1-Debian <<>> +trace google.com
;; global options: +cmd
.                       80475   IN      NS      i.root-servers.net.
.                       80475   IN      NS      e.root-servers.net.
.                       80475   IN      NS      l.root-servers.net.
.                       80475   IN      NS      b.root-servers.net.
.                       80475   IN      NS      h.root-servers.net.
.                       80475   IN      NS      m.root-servers.net.
.                       80475   IN      NS      c.root-servers.net.
.                       80475   IN      NS      k.root-servers.net.
.                       80475   IN      NS      j.root-servers.net.
.                       80475   IN      NS      f.root-servers.net.
.                       80475   IN      NS      d.root-servers.net.
.                       80475   IN      NS      a.root-servers.net.
.                       80475   IN      NS      g.root-servers.net.
.                       514520  IN      RRSIG   NS 8 0 518400 20261102170000 20261020160000 8763 . TX7ZWI773drtn2wJRoAxbHs/xVglRtCZ3CSA9T/h5v0w9a0Hh6HM0NuU gCIQPYq2f9dG2rvuIDWBuG94m+KKvYwZCnUghd+ZLCQndZdEXN16HTQN ESKQhHgJmFI7uFpc5sIJcaYzrZojcDA+YI4x75M1M/IPLPxqFdBVzneS 5Xd+d4aWHQIy+mt1ineaJ8OZAeQMfg3DJ4mtMy3X+Z0mgg92zJKk1tRH jtdzAM643Xia5tcteh31buC+4c4ZYVa8E/JwdgwBxgNJo3XAkcJPEaf8 FQiK6TnGDxfSgmJahFmDxUwEbgVXx6tPhiMONwBtkqeIq54LalM5RXx9 nJVCrg==
;; Received 1137 bytes from 192.168.1.1#53(192.168.1.1) in 16 ms

;; UDP setup with 2801:1b8:10::b#53(2801:1b8:10::b) for google.com failed: network unreachable.
;; no servers could be reached
;; UDP setup with 2801:1b8:10::b#53(2801:1b8:10::b) for google.com failed: network unreachable.
;; no servers could be reached
;; UDP setup with 2801:1b8:10::b#53(2801:1b8:10::b) for google.com failed: network unreachable.
com.                    172800  IN      NS      a.gtld-servers.net.
com.                    172800  IN      NS      b.gtld-servers.net.
com.                    172800  IN      NS      c.gtld-servers.net.
com.                    172800  IN      NS      d.gtld-servers.net.
com.                    172800  IN      NS      e.gtld-servers.net.
com.                    172800  IN      NS      f.gtld-servers.net.
com.                    172800  IN      NS      g.gtld-servers.net.
com.                    172800  IN      NS      h.gtld-servers.net.
com.                    172800  IN      NS      i.gtld-servers.net.
com.                    172800  IN      NS      j.gtld-servers.net.
com.                    172800  IN      NS      k.gtld-servers.net.
com.                    172800  IN      NS      l.gtld-servers.net.
com.                    172800  IN      NS      m.gtld-servers.net.
com.                    86400   IN      DS      19718 13 2 8ACBB0CD28F41250A80A491389424D341522D946B0DA0C0291F2D3D7 71D7805A
com.                    86400   IN      RRSIG   DS 8 1 86400 20261102200000 20261020190000 8763 . bPsoGel8XclMSTifM7SHlcRItu73aP89lhprXkvJfCqZ+jItN6B9Im48 Wn4gmOiJPbTKARkCYVElEfc+qc9dsJvpebPwix5f4MqSyNCFu4WZqUv0 xCNCHGsVmz1cWJze0slFrSvKTjdMp/7ZEt2d52qKO+ZWrg+fswCwSUZ6 NW0zjL87NerODK2XlwKpj9ac6znJjaVVAqeCDsB/+aSf1dOHgHy5O+k+ DhHf94GZzB9sCXydCwtGIMY4O/0sW/ql48nlxqpgFgdQ15oCgUwH8n7h aEJ+wF57iEPrz8dOIsmsriyToJthstVrW39RASg7T1bLlDhH5UEJOCT4 BRoVZA==
;; Received 1170 bytes from 192.58.128.30#53(j.root-servers.net) in 252 ms

google.com.             172800  IN      NS      ns2.google.com.
google.com.             172800  IN      NS      ns1.google.com.
google.com.             172800  IN      NS      ns3.google.com.
google.com.             172800  IN      NS      ns4.google.com.
CK0POJMG874LJREF7EFN8430QVIT8BSM.com. 900 IN NSEC3 1 1 0 - CK0Q35HRS4H76G6CHNB9414CJN6S5UPL NS SOA RRSIG DNSKEY NSEC3PARAM
CK0POJMG874LJREF7EFN8430QVIT8BSM.com. 900 IN RRSIG NSEC3 13 2 900 20261025002615 20261017231615 65344 com. /N6fN5DVPuyLATL2Ja4dJ2NW3hEzenqQS7D9W+3h1zxvdSlTmVLXpce2 b4naOr0/JAvD4mKcI2WPEjH89beg/g==
S84BOR4DK28HNHPLC218O483VOOOD5D8.com. 900 IN NSEC3 1 1 0 - S84BR9CIB2A20L3ETR1M2415ENPP99L8 NS DS RRSIG
S84BOR4DK28HNHPLC218O483VOOOD5D8.com. 900 IN RRSIG NSEC3 13 2 900 20261026012150 20261019001150 65344 com. Bjj5dOkBIXH2m7/xENpspvmCc125ivCuxdk3Hxm/eHhXzDh+0O/7s+u4 hOZopnZhVdT0HGBmap7UDmGAdPZKGg==
;; Received 644 bytes from 192.35.51.30#53(f.gtld-servers.net) in 204 ms

;; UDP setup with 2001:4860:4802:34::a#53(2001:4860:4802:34::a) for google.com failed: network unreachable.
google.com.             300     IN      A       142.251.37.142
;; Received 55 bytes from 216.239.36.10#53(ns3.google.com) in 164 ms
```

### C. `dnsrecon -d tesla.com -t std` (Standard Enumeration)
*Annotation:* This reveals Tesla's nameservers (Akamai), MX records (Outlook), and a ton of TXT records, including a `bugcrowd-verification` record.

```text
[*] std: Performing General Enumeration against: tesla.com...
[-] DNSSEC is not configured for tesla.com
[*]      SOA edns69.ultradns.com 204.74.66.69
[*]      SOA edns69.ultradns.com 2001:502:f3ff::245
[*]      NS a9-67.akam.net 184.85.248.67
[*]      Bind Version for 184.85.248.67 "53569.212"
[*]      NS a9-67.akam.net 2a02:26f0:117::43
[*]      NS a7-66.akam.net 23.61.199.66
[*]      Bind Version for 23.61.199.66 "53569.212"
[*]      NS a7-66.akam.net 2600:1406:32::42
[*]      NS edns69.ultradns.com 204.74.66.69
[*]      Bind Version for 204.74.66.69 Nameserver"
[*]      NS edns69.ultradns.com 2001:502:f3ff::245
[*]      NS a28-65.akam.net 95.100.173.65
[*]      Bind Version for 95.100.173.65 "53050.171"
[*]      NS a28-65.akam.net 2600:1480:d800::41
[*]      NS a12-64.akam.net 184.26.160.64
[*]      Bind Version for 184.26.160.64 "53050.172"
[*]      NS a12-64.akam.net 2600:1480:f000::40
[*]      NS a10-67.akam.net 96.7.50.67
[*]      Bind Version for 96.7.50.67 "53050.171"
[*]      NS a10-67.akam.net 2600:1480:d000::43
[*]      NS a1-12.akam.net 193.108.91.12
[*]      Bind Version for 193.108.91.12 "53569.213"
[*]      NS a1-12.akam.net 2600:1401:2::c
[*]      MX tesla-com.mail.protection.outlook.com 52.101.60.179
[*]      MX tesla-com.mail.protection.outlook.com 52.101.40.26
[*]      MX tesla-com.mail.protection.outlook.com 52.101.60.148
[*]      MX tesla-com.mail.protection.outlook.com 52.101.60.65
[*]      A tesla.com 2.18.49.207
[*]      A tesla.com 23.40.100.207
[*]      A tesla.com 2.18.52.207
[*]      A tesla.com 2.18.53.207
[*]      A tesla.com 2.18.54.207
[*]      A tesla.com 2.18.55.207
[*]      A tesla.com 2.18.50.207
[*]      A tesla.com 2.18.51.207
[*]      A tesla.com 23.7.244.207
[*]      A tesla.com 2.18.48.207
[*]      TXT tesla.com domain-verification=0f075f7f33bd0e577c0a56c5bb071f9eedadba45f32da11304913c6afd4b99c7
[*]      TXT tesla.com 55zNJIDU0xk94IfGJtL+Hh+wje5JzOS6GY+ntggZF908AUsx0LBKgr+Nln3CgZEUifxSuN09M05jYpdbd6+cpw==
[*]      TXT tesla.com atlassian-domain-verification=FuJL8qfcWp7BKpnaomRV1Vmay09Vt0rdhikq9Gh/CwPYjsvTIwkrhaVAX1idqUMl
[*]      TXT tesla.com atlassian-domain-verification=U31RjXDO5NBJROoOVpVEsKJ7daGpXuXPDF8HeqlmvXUKOtTao652TOMtejHrohKB
[*]      TXT tesla.com dell-technologies-domain-verification=tesla.com_c363f56d-9650-430a-82d3-04ac2257c64a_1756487968
[*]      TXT tesla.com v=spf1 ip4:54.240.84.225/32 ip4:54.240.84.226/31 ip4:54.240.84.228/30 ip4:54.240.84.232/29 ip4:54.240.84.240/29 ip4:54.240.84.248/30 ip4:54.240.84.252/32 ip4:44.239.249.139 ip4:52.24.70.112 ip4:34.223.204.78 ip4:213.244.145.203 ip4:213.244.145.219 ip4:213.244.145.204 ip4:213.244.145.220 ip4:8.47.24.203 ip4:8.47.24.219 ip4:8.47.24.204 ip4:8.47.24.220 ip4:8.45.124.203 ip4:8.45.124.219 ip4:8.45.124.204 ip4:8.45.124.220 ip4:8.21.14.203 ip4:8.21.14.219 ip4:8.21.14.204 ip4:8.21.14.220 ip4:8.21.14.194 ip4:8.21.14.211 ip4:212.49.145.0/24 ip4:91.103.52.0/22 ip4:168.245.123.10 ip4:216.81.144.165 ip4:149.72.247.52 ip4:149.72.134.64 ip4:149.72.152.236 ip4:149.72.163.58 ip4:149.72.172.170 ip4:167.89.90.62 ip4:158.228.129.79 ip4:216.81.144.165 ip4:117.50.14.178 ip4:117.50.35.199 ip4:54.240.42.110 ip4:54.240.42.111 ip4:199.71.239.178 ip4:67.216.183.10 ip4:8.43.178.222 ip4:64.95.144.196 ip4:199.71.239.52 include:u13494342.wl093.sendgrid.net include:spf.protection.outlook.com include:mail.zendesk.com include:_spfsn.teslamotors.com include:_spf.qualtrics.com include:_spf.ultipro.com include:_spf.psm.knowbe4.com include:spf1.sendcloud.org include:spf2.sendcloud.org -all
[*]      TXT tesla.com T0E0S29854
[*]      TXT tesla.com MS=ms22358213
[*]      TXT tesla.com _f32sd18rpksw3zh1hgbhaulpv016hoh
[*]      TXT tesla.com _i88zzpi9e3jr0xglot953efk0ui36y5
[*]      TXT tesla.com _owlpg4menxk5zjwee9xclui989imwbl
[*]      TXT tesla.com _quuerjb9mywulmdygnzgnt9awyzm15c
[*]      TXT tesla.com _w19nckjurfa4aldim48vtbrxsq1phnv
[*]      TXT tesla.com apple-domain-verification=C9J7eOtEbm7Dqr88
[*]      TXT tesla.com SFMC-qkAv7SvlQaslp7NEALX8t68s_AZWOQB6ThKQS5l5
[*]      TXT tesla.com jamf-site-verification=u4x3LuqSfpoLn5nJ0zMd5g
[*]      TXT tesla.com logmein-domain-confirmation=9zxwVn2buGWrLtU24J88
[*]      TXT tesla.com logmein-verification-code=JFAnsPovogeJ4IeW5MXCU3r0C
[*]      TXT tesla.com traction-guest=b4f7ad59-bf17-4b3c-8b36-9c2d28f1de32
[*]      TXT tesla.com traction-guest=c8bad9fc-4b36-4f6d-944e-783ed41b34b7
[*]      TXT tesla.com bugcrowd-verification=40bd5dd89a6e4073ca9bc76feac3a47b
[*]      TXT tesla.com adobe-sign-verification=efb2da198047b7a154bd604d2721038b
[*]      TXT tesla.com docker-verification=74d1ec4e-a7a6-48a7-9568-9bd0faac833f
[*]      TXT tesla.com cloudflare_dashboard_sso=5c0b681b716d2de0666f5a564a4d9c0d
[*]      TXT tesla.com cursor-domain-verification-6kgt2s=sxbxrRmk2tNjItWtmh1swmBM0
[*]      TXT tesla.com ms-domain-verification=820e4be7-563e-4f52-b73a-5c9ecdd2fda4
[*]      TXT tesla.com ms-domain-verification=e335cec9-0ff5-4a54-b8bc-8966a8d146db
[*]      TXT tesla.com teamviewer-sso-verification=2fc989f75b19494fab5eb0e2c22dd625
[*]      TXT tesla.com onetrust-domain-verification=480735b10e124e23916192d7e4321902
[*]      TXT tesla.com onetrust-domain-verification=79a1328740f44bc48dd97ab52c0c3377
[*]      TXT tesla.com adobe-idp-site-verification=321c026a-3a8c-4206-a1fa-391a59585c54
[*]      TXT tesla.com google-site-verification=Xg2DEUg2oCz1q9RMx8gh2htHK16_GG9cZXY_eyeSf6w
[*]      TXT tesla.com google-site-verification=Y7lbse5bSatjXaqSBOWXjsit4mOp9cQzfLDpnQUSZlg
[*]      TXT tesla.com apple-domain-verification=CHZ8RLPKu4dlRxlaNa_nR9oA2MjZ1n2fiE9s0QlbRO8
[*]      TXT tesla.com google-site-verification=f1YoSQ3nrxPHwlfkwT9Mj_7M_rzQ2RqCPBYHJ9CQNlY  
[*]      TXT tesla.com zapier-domain-verification-challenge=64e810e8-0fe1-4de0-b104-229592811c5b
[*]      TXT _dmarc.tesla.com v=DMARC1; p=reject; pct=100; rua=mailto:n2ju30bc@ag.dmarcian.com; ruf=mailto:n2ju30bc@fr.dmarcian.com; fo=1
[*] Enumerating SRV Records
[+]      SRV _sipfederationtls._tcp.tesla.com sipfed.online.lync.com 52.123.173.219 5061
[+] 1 Records Found
```

### D. `amass enum -passive -d tesla.com` (Passive Subdomain Enumeration)
*Annotation:* Amass maps the attack surface by finding subdomains and their CNAME records. Notice how many subdomains point to Akamai (`edgekey.net`) or AWS (`amazonaws.com`).

```text
tesla.com (FQDN) --> ns_record --> a1-12.akam.net (FQDN)
tesla.com (FQDN) --> ns_record --> a7-66.akam.net (FQDN)
tesla.com (FQDN) --> ns_record --> a9-67.akam.net (FQDN)
tesla.com (FQDN) --> ns_record --> a10-67.akam.net (FQDN)
tesla.com (FQDN) --> ns_record --> a12-64.akam.net (FQDN)
tesla.com (FQDN) --> ns_record --> a28-65.akam.net (FQDN)
tesla.com (FQDN) --> ns_record --> edns69.ultradns.com (FQDN)
tesla.com (FQDN) --> mx_record --> tesla-com.mail.protection.outlook.com (FQDN)
mobile-links.prd.vn.cloud.tesla.com (FQDN) --> cname_record --> npuca-prd.usw.vn.cloud.tesla.com (FQDN)
gateway-public-telemetry-prd5a-fleet.prd.vn.cloud.tesla.com (FQDN) --> cname_record --> usw-prd5a-fleet-gpute-prd.teslafleet.akadns.net (FQDN)
media-server-api.prd.vn.cloud.tesla.com (FQDN) --> cname_record --> usw-prd5x-media-gpuca-prd.teslafleet.akadns.net (FQDN)
apf-api.prd.vn.cloud.tesla.com (FQDN) --> cname_record --> fleet-apf-prd.tesla.com (FQDN)
apac-cppm.tesla.com (FQDN) --> cname_record --> apac-cppm.tesla.com.srip.net (FQDN)
apf-api.eng.vn.cloud.tesla.com (FQDN) --> cname_record --> fleet-apf-eng.tesla.com (FQDN)
apmv3-cdn-go.tesla.com (FQDN) --> cname_record --> apmv3.tesla.com.akadns.net (FQDN)
livestream.tesla.com (FQDN) --> cname_record --> livestream.tesla.com-v1.edgekey.net (FQDN)
bolt.tesla.com (FQDN) --> cname_record --> bolt.tesla.com.edgekey.net (FQDN)
static-assets-teslaaccount.tesla.com (FQDN) --> cname_record --> external-na-pop1.edgekey.net (FQDN)
serviceapi-stg.tesla.com (FQDN) --> cname_record --> serviceapi-stg.tesla.com.edgekey.net (FQDN)
bettertime-stage.tesla.com (FQDN) --> cname_record --> bettertime-stage.tesla.com.edgekey.net (FQDN)
hermes-api.prd.na.vn.cloud.tesla.com (FQDN) --> cname_record --> usw-prd5x-hermes-npuhe-prd.teslafleet.akadns.net (FQDN)
tripx.prd.vn.cloud.tesla.com (FQDN) --> cname_record --> npuca-prd.usw.vn.cloud.tesla.com (FQDN)
livestream.tesla.com-v1.edgekey.net (FQDN) --> cname_record --> e1792.dscx.akamaiedge.net (FQDN)
external-na-pop1.edgekey.net (FQDN) --> cname_record --> e1792.dscx.akamaiedge.net (FQDN)
fleet-api.prd.na.vn.cloud.tesla.com (FQDN) --> cname_record --> epuca-prd.usw.vn.cloud.tesla.com (FQDN)
powerhub.energy.tesla.com (FQDN) --> cname_record --> powerhub.sn.tesla.services (FQDN)
apigateway-supplierprofileapi-stg.tesla.com (FQDN) --> cname_record --> apigateway-edge.tesla.com.edgekey.net (FQDN)
device-api.prd.na.vn.cloud.tesla.com (FQDN) --> cname_record --> npuv-prd.usw.vn.cloud.tesla.com (FQDN)
edr.tesla.com (FQDN) --> cname_record --> edr.tesla.com-v1.edgekey.net (FQDN)
live-data.america.fn.tesla.com (FQDN) --> cname_record --> live-data.prd.america.fn.tesla.com (FQDN)
live-data.fn.tesla.com (FQDN) --> cname_record --> live-data.europe.fn.tesla.com (FQDN)
autobidder-preprd.powerhub.energy.tesla.com (FQDN) --> cname_record --> energy.tesla.com.edgekey.net (FQDN)
api-toolbox.tesla.com (FQDN) --> cname_record --> api.toolbox.tb.tesla.services (FQDN)
business-fulfillment-assets.tesla.com (FQDN) --> cname_record --> business-fulfillment-assets.tesla.com.edgekey.net (FQDN)
apigateway-energy-fulfillment-cx-bff-prd.tesla.com (FQDN) --> cname_record --> apigateway-energy-fulfillment-cx-bff-prd.tesla.com.edgekey.net (FQDN)
e-repair.tesla.com (FQDN) --> cname_record --> external-na-pop1.edgekey.net (FQDN)
akamai-apigateway-teslarpsapi.tesla.com (FQDN) --> cname_record --> akamai-apigateway-teslarpsapi.tesla.com.edgekey.net (FQDN)
origin-installations-ext-api.tesla.com (FQDN) --> cname_record --> clsmdcegyp.tesla.com.akadns.net (FQDN)
email.satish.tesla.com (FQDN) --> cname_record --> www.tesla.com (FQDN)
origin-assets-contactus.tesla.com (FQDN) --> cname_record --> origin-assets-contactus.tesla.com.edgekey.net (FQDN)
s3.eng.na.vn.cloud.tesla.com (FQDN) --> cname_record --> gpuca-eng.usw.vn.cloud.tesla.com (FQDN)
fsx.tesla.com (FQDN) --> cname_record --> external-eu-pop.edgekey.net (FQDN)
tcc-gw-stg.tesla.com (FQDN) --> cname_record --> external-na-pop1.edgekey.net (FQDN)
pages.emails.tesla.com (FQDN) --> cname_record --> pages.virt.s10.exacttarget.com (FQDN)
akamai-apigateway-vfx.tesla.com (FQDN) --> cname_record --> akamai-apigateway-vfx.tesla.com.edgekey.net (FQDN)
apigateway-track-bff.tesla.com (FQDN) --> cname_record --> apigateway-edge.tesla.com.edgekey.net (FQDN)
akamai-ap