# HTTP Idempotence
A web server may contain many features which will fulfill user's need. Some of the operation could have resources and it also could contain functions to modify the resources state. Because those resources may be important, any unintended change must be avoided.

For example if a user want to withdraw money, it must only accomplished once on that session. Any duplicate action caused by retrying the process either intentionaly or unintentionaly unexpected error, still should produce outcome like when the user succesfully withdraw once. So withdrawing money repeatedly by mistake will be prevented by the system.

Such feature can be achieved by implementing idempotence to the web server. By definition, idempotence is a property of an operation whereby it can be performed several times but the result is always the same. In HTTP, there are default idempotence method such as described by the table below:

| Method | Idempotence | 
| - | :-: |
| GET | Yes |
| PUT | Yes |
| DELETE | Yes* |
| POST | No |
| PATCH | No* |

The DELETE method is idempotence as long as the delete operation is having an identifier, not by deleting on entries position such as on every first entry or every last entry. The PATCH method is not idempotence if the updated resources is appended/deducted based on it is previous values. Lastly, the rest non idempotence HTTP methods should be implemented manualy when building the system.

## Solution
1. Generate an "idempotency key" element, the key should be unique to avoid collisions (e.g. using V4 UUID).
1. Client put the key to be included on the request.
1. Server then will save the result of the operation on first completed request, identified by given idempotency key.
1. The key may be saved by the server on configured period, then it could be pruned afterward.
1. Any subsequent requests with the same key will return the same result, or resulting some kind of error to the client (e.g. error code 409).

## Example App
App to simulate Idempotency is available made with Python Flask (as backend) and Svelte (as frontend).

### Backend
1. Made using Python v3.12+
2. Install dependencies by `pip install -r requirements.txt`
3. Run development server by `flask --app server run`
4. App will be started at `localhost:5000`
5. Hit HTTP endpoint `/init-db` to initialize SQLite database

### Frontend
1. Made using NodeJS v18+
2. Install dependencies by `npm install`
3. Run development app by `npm run dev`
4. App will be started at `localhost:5173`