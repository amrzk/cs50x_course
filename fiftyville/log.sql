-- crime_scene_reports (id and description) on the date and location of the crime July 28, 2021, Humphrey Street (incident report)
SELECT id, description
FROM crime_scene_reports
WHERE day = 28
AND month = 7
AND year = 2021
AND street = 'Humphrey Street';
    -- | 295 | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
    -- Interviews were conducted today with three witnesses who were present at the time
    -- each of their interview transcripts mentions the bakery.
-------------------------

-- checking interviews on the date of the crime (witnesses)
SELECT id, name, transcript
FROM interviews
WHERE day = 28
AND month = 7
AND year = 2021
AND transcript LIKE '%bakery%';
    -- | 161 | Ruth    | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
        -- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

    -- | 162 | Eugene  | I don't know the thief's name, but it was someone I recognized.
        -- Earlier this morning, before I arrived at Emm.a's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

    -- | 163 | Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
        -- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
        -- The thief then asked the person on the other end of the phone to purchase the flight ticket.
-------------------------

-- following on on Ruth's interview (license plates of suspects)
SELECT id, license_plate
FROM bakery_security_logs
WHERE day = 28
AND month = 7
AND year = 2021
AND hour = 10
AND minute >= 5
AND minute <= 25
AND activity = 'exit';
    -- | id  | license_plate |
    -- | 260 | 5P2BI95       |
    -- | 261 | 94KL13X       |
    -- | 262 | 6P58WS2       |
    -- | 263 | 4328GD8       |
    -- | 264 | G412CB7       |
    -- | 265 | L93JTIZ       |
    -- | 266 | 322W7JE       |
    -- | 267 | 0NTHK55       |
-------------------------

-- following on on Eugene's interview (bank account number of suspects)
SELECT id, account_number, amount
FROM atm_transactions
WHERE day = 28
AND month = 7
AND year = 2021
AND atm_location ='Leggett Street'
AND transaction_type ='withdraw';
    -- | id  | account_number | amount |
    -- | 246 | 28500762       | 48     |
    -- | 264 | 28296815       | 20     |
    -- | 266 | 76054385       | 60     |
    -- | 267 | 49610011       | 50     |
    -- | 269 | 16153065       | 80     |
    -- | 288 | 25506511       | 20     |
    -- | 313 | 81061156       | 30     |
    -- | 336 | 26013199       | 35     |
-------------------------

-- following on on Raymond's interview
    -- | 163 | Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
        -- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
        -- The thief then asked the person on the other end of the phone to purchase the flight ticket.
        --  (phone call)
SELECT id, caller, receiver
FROM phone_calls
WHERE day = 28
AND month = 7
AND year = 2021
AND duration < 60;
    -- | id  |     caller     |    receiver    |
    -- | 221 | (130) 555-0289 | (996) 555-8899 |
    -- | 224 | (499) 555-9472 | (892) 555-8872 |
    -- | 233 | (367) 555-5533 | (375) 555-8161 |
    -- | 251 | (499) 555-9472 | (717) 555-1342 |
    -- | 254 | (286) 555-6063 | (676) 555-6554 |
    -- | 255 | (770) 555-1861 | (725) 555-3243 |
    -- | 261 | (031) 555-6622 | (910) 555-3251 |
    -- | 279 | (826) 555-1652 | (066) 555-9701 |
    -- | 281 | (338) 555-6650 | (704) 555-2131 |

        --  (flight)
SELECT flights.id, airports.abbreviation, airports.full_name, airports_2.abbreviation, airports_2.full_name, airports_2.city, hour, minute
FROM flights
    JOIN airports
    ON airports.id = flights.origin_airport_id
    JOIN airports as airports_2
    ON airports_2.id = flights.destination_airport_id
WHERE day = 29
AND month = 7
AND year = 2021
ORDER BY hour, minute
LIMIT 1;
    -- | id | abbreviation |          full_name          | abbreviation |     full_name     |     city      | hour | minute |
    -- | 36 | CSF          | Fiftyville Regional Airport | LGA          | LaGuardia Airport | New York City | 8    | 20     |

        -- (passengers)
SELECT passport_number, seat
FROM passengers
WHERE flight_id = (
    SELECT id
    FROM flights
    WHERE day = 29
    AND month = 7
    AND year = 2021
    ORDER BY hour, minute
    LIMIT 1
    );
    -- | passport_number | seat |
    -- | 7214083635      | 2A   |
    -- | 1695452385      | 3B   |
    -- | 5773159633      | 4A   |
    -- | 1540955065      | 5C   |
    -- | 8294398571      | 6C   |
    -- | 1988161715      | 6D   |
    -- | 9878712108      | 7A   |
    -- | 8496433585      | 7B   |

------------------------------
-- the thief is whom ever has (license plate, bank account number ,caller number, passport number)
        -- (license plate)
SELECT people.id, people.name, people.phone_number
FROM people
INNER JOIN bakery_security_logs
ON people.license_plate = bakery_security_logs.license_plate
INNER JOIN bank_accounts
On people.id = bank_accounts.person_id
INNER JOIN atm_transactions
ON bank_accounts.account_number = atm_transactions.account_number
INNER JOIN phone_calls
ON people.phone_number = phone_calls.caller
INNER JOIN passengers
ON people.passport_number = passengers.passport_number
--
WHERE bakery_security_logs.day = 28
    AND bakery_security_logs.month = 7
    AND bakery_security_logs.year = 2021
    AND bakery_security_logs.hour = 10
    AND bakery_security_logs.minute >= 5
    AND bakery_security_logs.minute <= 25
    AND bakery_security_logs.activity = 'exit'
--
    AND atm_transactions.day = 28
    AND atm_transactions.month = 7
    AND atm_transactions.year = 2021
    AND atm_transactions.atm_location ='Leggett Street'
    AND atm_transactions.transaction_type ='withdraw'
--
    AND phone_calls.day = 28
    AND phone_calls.month = 7
    AND phone_calls.year = 2021
    AND phone_calls.duration < 60
--
    AND passengers.flight_id = (
        SELECT id
        FROM flights
        WHERE flights.day = 29
        AND flights.month = 7
        AND flights.year = 2021
        ORDER BY flights.hour, flights.minute
        LIMIT 1
        );
--
    -- |   id   | name  |  phone_number  |
    -- +--------+-------+----------------+
    -- | 686048 | Bruce | (367) 555-5533 |
------------------------------

-- the accomplice is whom ever has (Bruce called, ...)
-- following on on Raymond's interview
    -- | 163 | Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
        -- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
        -- The thief then asked the person on the other end of the phone to purchase the flight ticket.
        --  (phone call)

SELECT people.id, people.name, people.phone_number
FROM people
INNER JOIN phone_calls
ON people.phone_number = phone_calls.receiver
WHERE phone_calls.day = 28
AND phone_calls.month = 7
AND phone_calls.year = 2021
AND phone_calls.duration < 60
AND phone_calls.caller = '(367) 555-5533';

    -- |   id   | name  |  phone_number  |
    -- +--------+-------+----------------+
    -- | 864400 | Robin | (375) 555-8161 |
------------------------------