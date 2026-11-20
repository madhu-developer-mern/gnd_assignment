# gnd_assignment

Implement three API endpoints in the provided Django project. Use Python 3.11 or newer and an internet connection to install dependencies.

## Get started

```sh
git clone https://github.com/madhu-developer-mern/gnd_assignment.git
cd gnd_assignment
python manage.py setup
```

Setup creates `.venv`, installs the pinned dependencies, and prepares a local SQLite database with 20 sample products. Start the API with `python manage.py runserver`. It listens at `http://127.0.0.1:8000`.

To use Postman, import the collection and `Local.postman_environment.json` from `Django-Backend-Assessment/project/postman` and select the **Local** environment.

## Your assignment

Search for `TODO: Candidate implementation` in `Django-Backend-Assessment/project`. The paths below are relative to that folder.

| Endpoint | Where to write code |
| --- | --- |
| `POST /api/register/` | `accounts/serializers.py` (`RegistrationSerializer.validate` and `create`) and `accounts/views.py` (`RegistrationView.post`) |
| `GET /api/items/` | `products/serializers.py` (`PaginationSerializer`), `products/services.py` (`list_items`), and `products/views.py` (`ItemView.get`) |
| `QUERY /api/items/` | `products/serializers.py` (`ItemFilterSerializer`), `products/services.py` (`filter_items`), and `products/views.py` (`ItemView.query`) |

The starter endpoints return HTTP 501. Run `python manage.py test` from the repository root to check your implementation. Leave the provided tests as supplied.

## API contract

Requests with bodies use `Content-Type: application/json`. Invalid input returns HTTP 400 with field-keyed error arrays. Malformed JSON also returns HTTP 400.

### `POST /api/register/`

Send four required JSON strings.

```json
{
  "name": " Madhu ",
  "email": "MADHU@example.com",
  "phone_number": "0987654321",
  "password": "Password@123"
}
```

- Trim the name before validating its 1–20 character length.
- Validate email format and a 100-character maximum. Lowercase it and enforce uniqueness, including when the database detects a conflict during save.
- Require exactly 10 ASCII digits in the phone number and enforce uniqueness. Preserve leading zeroes.
- Require an 8–30 character password with an uppercase letter, a lowercase letter, a digit, and a non-whitespace special character. Save a Django password hash.

On success return HTTP 201 with `id`, `name`, `email`, `phone_number`, and the message `User registered successfully`.

### `GET /api/items/`

Return HTTP 200 with a JSON array in ascending ID order. Without pagination parameters return all items. If either parameter is present, use `page=1` and `page_size=10` for any omitted values. Both must be positive integers and page size is capped at 100. A page past the end returns an empty array.

Both item endpoints return `id`, `name`, `description`, `category`, `brand`, `price`, `discount_percentage`, `stock_quantity`, `rating`, `is_available`, `created_at`, and `updated_at`. Price and rating are JSON numbers. Timestamps are ISO 8601 strings.

### `QUERY /api/items/`

Use the literal HTTP method **QUERY** with an optional JSON object. An empty object or an omitted body matches all items. Apply all supplied filters together and return HTTP 200 with `{"total": 2, "items": [...]}`, where `total` equals the number of returned items. Keep the ascending ID order and leave the database untouched.

| Filters | Meaning |
| --- | --- |
| `name` | Case-insensitive substring |
| `category`, `brand` | Case-insensitive exact matches |
| `min_price`, `max_price` | Inclusive bounds, non-negative, up to two decimal places |
| `min_rating`, `max_rating` | Inclusive bounds from 0 to 5, up to two decimal places |
| `min_discount`, `max_discount` | Inclusive whole percentages from 0 to 100 |
| `in_stock` | JSON boolean. True means quantity above zero. False means zero. |
| `is_available` | JSON boolean matching the availability field |

Reject unknown filter names, reversed ranges, and non-object JSON bodies.

```json
{
  "category": "Electronics",
  "min_price": 2000,
  "max_price": 10000,
  "min_rating": 4,
  "in_stock": true
}
```

This example matches Wireless Headphones and Smart Watch.
