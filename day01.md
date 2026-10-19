# Day 1 - Foundation Corrections, HTTP Theory, and Curl

## 1. Foundation Corrections

### DNS Resolver
1. Checking Browser cache for the IP.
2. OS Cache - check if IP saved or not.
3. If DNS resolver does not have the IP, it queries the chain (like 8.8.8.8).
4. Root servers -> .com TLD (Top Level Domain).
5. TLD tells where the Authoritative nameserver is.
6. Authoritative Nameserver provides the requested DNS record (e.g., Google's IP).
7. Return IP to our computer and device to connect with the server.
*(Note: NOT ALWAYS does the resolver go to the Authoritative Name server due to caching).*

### HTTP/1.1 and Headers
- HTTP/1.1 is a protocol which transfers data between web browsers and servers.
- Headers are inside the protocol, which include Host, Cookies, and User Agents.

### Python r.status_code
- Checks for status code (like e.g., 201 Created, 403 Forbidden, 500 Internal Server Error).
- `r.json()` parses the response body.
- Status code is the metadata. The body is the data.

---

## 2. HTTP/1.1 vs HTTP/2 Summary

1. **Persistent Connections & Multiplexing:** HTTP/1.1 uses multiple connections for sequential requests; it waits for a sequence response, then the next request/response shows. HTTP/2 is used to make multiple requests over a single TCP connection, which is usually much faster.
2. **Header Compression (HPACK):** HTTP/2 uses HPACK to compress headers, reducing the effect of sending the same info over the internet again and again.
3. **Binary Framing:** HTTP/1.1 uses text format (readable data), but HTTP/2 uses the binary format to organize communication. It divides messages into smaller units called "frames" to organize communication.
4. **Head-of-Line Blocking:** HTTP/1.1 blocks other requests if one request is blocked; slow responses cause head-of-line blocking. HTTP/2 mitigates this by handling multiple requests over a single TCP connection.
5. **Request Handling:** HTTP/2 automatically sends requests for index.html and style.css. There is no need for separate requests as HTTP/1.1 does, just because of multiplexing, which sends multiple requests at a time over the same TCP connection.

---

## 3. Curl Commands and Flags

### Kali Linux Curl Basics
- **-v (verbose):** Force terminal to show everything sending and receiving. Without -v, only the response shows.
- **curl (Client-URL):** Command line tool without User Interface (UI).

### Flags & Commands
- **-I (HEAD):** Tells curl to simply give the response headers, ignores the body.
  - *Command:* `curl -I https://httpbin.org/status/404`

- **-s (SILENT):** Tells curl to clean the environment, not showing the progress or errors.
  - *Command:* `curl -s -o /dev/null -w "%{http_code}\n" https://httpbin.org/status/500`

- **-o /dev/null:** Output to a file just like a black hole. Data goes through it but disappears. Simply outputs to the blackhole file.
  - *Command:* `curl -s -o /dev/null -w "%{http_code}\n" https://httpbin.org/status/500`

- **-w "%{http_code}\n":** Write out. Tells curl to write out the code.
  - *Command:* `curl -s -o /dev/null -w "%{http_code}\n" https://httpbin.org/status/500`

---

## 4. Kali Linux Terminal Proof (Curl Screenshots)

**1. Full Curl -v Output (Part 1 - TLS Handshake):**
![Curl Verbose 1](<screenshots/Screenshot 2026-10-20 023047.png>)

**2. Full Curl -v Output (Part 2 - Request/Response Headers & JSON):**
![Curl Verbose 2](<screenshots/Screenshot 2026-10-20 023159.png>)

**3. Curl -I (HEAD Request) Output:**
![Curl HEAD Request](<screenshots/Screenshot 2026-10-20 023240.png>)

**4. Curl 404 Status Check:**
![Curl 404](<screenshots/Screenshot 2026-10-20 023306.png>)

**5. Curl -s -o /dev/null -w (Clean 500 Status Code):**
![Curl Silent Write Out](<screenshots/Screenshot 2026-10-20 023406.png>)