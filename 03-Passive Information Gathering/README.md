# Passive Information Gathering

PIG is the process of colleting information about your target using publicly available information, in other words, any act of gathering information about your target without communicating with them directly can de considered "passive". This could include services like:

* Search engine results
* **whois** information
* Background check services
* Public company information
* Forum posts

##### Te more information we manage to gather about our target, prior to our attack, the more likely we are to succeed.

Information-gathering in a penetration test is the most important phase. Knowing your target before attacking it is a proven recipe for success.

## 3.1 - Open Web Information Gathering

Once an engagement starts, it's important to first spend time browsing the web, looking for background information about the tarhet organization. 

* What do they do?
* How do they interact with the world?
* Do they have a sales department?
* Are they hiring?
* Email
* Phone
* Company structure

Sometimes, it's the smallest details that give you the most information: how well designed is the target website? How clean is their HTML code? This might give you a clue their web development budget, which may reflect on their security budget.

### 3.1.1 - Google

The Goole search engine is a security auditor's best friend.

#### 3.1.1.1 - Ennumerating with Google

Google supports the use of various search operators, wich allow a user to narrow down and pinpoint search results.

* site

> site:microsoft.com

The **site** operator will limit Google search results to a single domain. A simples search operator like this provide us with useful information.

* -site

> site:microsoft.com -site:www.microsoft.com

Remove **www** search