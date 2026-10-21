# Day 03 (Plan D01): HTTP Security Headers, Cookie Flags and SOP

Date: Oct 22, 2026
Repo numbering: Day 03. New plan numbering: D01 (first day of the merged plan).

## 1. Why HTTP security matters

Data moving between a browser and a server can be read or changed on the way. Three things protect it: security headers, secure cookie attributes, and HTTPS.

## 2. Security headers

Security headers are **response headers**. The server sends them to tell the browser how to handle the site's content and connections.

### 2.1 CSP (Content-Security-Policy)

- A response header from server to browser.
- Controls which resources and scripts the browser is allowed to load or execute.
- **Stops:** Cross-Site Scripting (XSS). Even if an attacker injects a script, the browser refuses to run it if the policy does not allow it.
- **Seen live:** on the Google results page, the console showed an error that an inline event handler violated the page's `script-src` directive, and that the action was blocked. That is CSP enforcing its policy in real time (see SS2).

### 2.2 HSTS (HTTP Strict-Transport-Security)

- Forces the browser to use HTTPS connections only.
- **Stops:** SSL stripping and downgrade attacks.
- Downgrade attack: the attacker forces the browser and server to drop the secure protocol, for example from HTTPS to HTTP.
- SSL stripping is a type of downgrade attack. The attacker sits in the middle as a proxy and steals credentials sent over the unencrypted connection.

### 2.3 X-Frame-Options

- Controls whether the browser may display the site inside a `<frame>` or `<iframe>` on another page.
- **Stops:** clickjacking. The victim thinks they click one thing, but the click lands on a hidden button of the framed site and triggers an action on their account.
- Common values: `DENY`, `SAMEORIGIN`.

### 2.4 X-Content-Type-Options

- With `nosniff` set, the browser must trust the declared Content-Type and must not guess the file type.
- **Stops:** MIME-sniffing attacks (for example, an uploaded file that is really a script being run because the browser guessed it was JavaScript).

## 3. Cookie attributes

Cookies are usually set in the `Set-Cookie` response header. The browser stores them and follows specific rules about when to send them back to the server.

### 3.1 HttpOnly

- Prevents client-side JavaScript from reading the cookie through `document.cookie`.
- **Stops:** session cookie theft through XSS. If the session ID cookie has HttpOnly, injected JavaScript cannot read it, so stealing the session is harder.

### 3.2 Secure

- Tells the browser to send the cookie only over HTTPS connections (localhost is an exception, for testing).
- **Stops:** session cookie interception on an unencrypted connection.
- Secure does **not** encrypt the cookie. HTTPS does that. Secure only controls when the cookie is sent.

### 3.3 SameSite

- Controls whether the browser sends the cookie with requests that come from another site.
- **Stops (partly):** Cross-Site Request Forgery (CSRF). The browser restricts sending the cookie with many cross-site requests.
- It is one layer of defence, not complete protection. CSRF tokens are still needed.
- Values: `Strict`, `Lax`, `None` (`None` requires `Secure`).

### 3.4 Sessions

HTTP is stateless, which means the server does not remember previous requests by itself. After login, the server creates a session ID and stores it in a cookie that the browser sends with each request. Anyone who gets this session ID may access my account, so `HttpOnly`, `Secure`, and `SameSite` help protect the session cookie.

### 3.5 Summary table

| Header / Flag | What it does | Attack it helps stop |
|---|---|---|
| Content-Security-Policy | Limits which scripts and resources can load | XSS |
| Strict-Transport-Security | Forces HTTPS | SSL stripping, downgrade |
| X-Frame-Options | Blocks framing by other pages | Clickjacking |
| X-Content-Type-Options | Disables content-type guessing | MIME sniffing |
| HttpOnly | JavaScript cannot read the cookie | Session theft via XSS |
| Secure | Cookie sent only over HTTPS | Cookie interception |
| SameSite | Restricts cross-site cookie sending | CSRF (partial) |

## 4. Header and cookie check on real sites (curl)

| Header / Flag | Wikipedia | OpenAI (`http://openai.com`) | Google |
|---|---|---|---|
| Content-Security-Policy (CSP) | Missing | Missing | Report-only present |
| X-Frame-Options | Missing | Missing | Present (`SAMEORIGIN`) |
| X-Content-Type-Options | Missing | Present (`nosniff`) | Missing |
| Strict-Transport-Security (HSTS) | Present | Missing in captured response | Missing in captured response |
| Set-Cookie | Present | Present | Present |
| Secure cookie flag | Present on some cookies | Missing in captured cookie | Present on some cookies |
| HttpOnly cookie flag | Present on some cookies | Present | Present on some cookies |
| SameSite cookie attribute | Present on some cookies | Missing in captured cookie | Present on some cookies |

### Notes

- Google has `Content-Security-Policy-Report-Only`, which reports policy violations but does not enforce the policy.
- OpenAI returned an HTTP redirect to HTTPS. The results above describe the captured HTTP response.
- Different cookies on the same website may have different security flags.
- Missing headers in the captured response do not prove that the website lacks all other security protections.
- The localhost cookie (no HttpOnly, no Secure) is covered in section 5.

## 5. Cookie storage inspection

![SS1: Firefox Storage tab on http://127.0.0.1:8000 with test_cookie selected and its flags shown in the detail pane](screenshots/day03-ss1-cookies-storage.png)

*SS1: Firefox DevTools > Storage > Cookies > `http://127.0.0.1:8000`, `test_cookie` selected. The right pane lists its flags.*

Flags on the localhost test cookie (`test_cookie=hello`):

- `HttpOnly: false`: JavaScript can read it with `document.cookie`.
- `Secure: false`: the browser sends it over plain HTTP.
- `SameSite: Lax`: not sent on most cross-site requests.
- `HostOnly: true`, `Path: /`, `Expires: Session`: only for `127.0.0.1`, whole site, deleted when the browser closes.
- This is a cookie with no HttpOnly and no Secure: the weak baseline to compare real sites against.

## 6. Same-Origin Policy (SOP)

### 6.1 Console test

Run from the console of a page on `https://www.google.com`:

```js
fetch("https://github.com").then(r => r.text()).then(console.log)
```

Result:

```
Promise {<pending>}
Access to fetch at 'https://github.com/' from origin 'https://www.google.com'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is
present on the requested resource.
GET https://github.com/ net::ERR_FAILED 200 (OK)
```

![SS2: console showing the CORS error for the cross-origin fetch](screenshots/day03-ss2-console-cors-error.png)

*SS2: Console output of the blocked cross-origin fetch.*

### 6.2 Reading the output

- `Promise {<pending>}`: the request started but never resolved with data.
- `blocked by CORS policy`: GitHub's response had no `Access-Control-Allow-Origin` header allowing `google.com`, so the browser did not hand the response to the script.
- `GET https://github.com/ ... 200 (OK)`: GitHub **did answer with 200 OK**. The request was sent and the server replied. The browser then hid the reply from JavaScript.

### 6.3 SOP in my own words

The Same-Origin Policy (SOP) is a browser security rule that protects users by stopping one website from freely accessing sensitive data from another website. By default, a webpage can access resources from the same origin, which includes the same protocol, domain, and port. For example, it helps prevent a malicious website from reading private information from another website. CORS (Cross-Origin Resource Sharing) allows a server to permit access from other origins through specific HTTP headers.

Evidence from SS2: the request to GitHub still got `200 (OK)`, but the browser blocked my script from reading the reply because GitHub sent no `Access-Control-Allow-Origin` header for `google.com`.

## 7. Screenshot instructions

| SS | Filename | What must be visible | How to take it |
|---|---|---|---|
| SS1 | `screenshots/day03-ss1-cookies-storage.png` | The cookie row selected, its HttpOnly, Secure and SameSite values readable (table columns in Chrome, right detail pane in Firefox), and the site's URL in the address bar | Chrome: F12 > Application > Cookies > the domain. Firefox: F12 > Storage > Cookies > the domain, then click the cookie row. If the table is empty, reload with the panel open. |
| SS2 | `screenshots/day03-ss2-console-cors-error.png` | The `fetch(...)` line you typed, `Promise {<pending>}`, the CORS error, and the `net::ERR_FAILED 200 (OK)` line | Already taken. Keep as is. |

## 8. Proof checklist

- [ ] `day03.md` (this file) in the repo root, next to `day01.md` and `day02.md`
- [ ] SS1 shows the cookie table, not an empty panel
- [ ] SS2 in `screenshots/`

