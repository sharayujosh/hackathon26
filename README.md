## Inspiration
Every time care is administered to a patient, nurses must gather dozens of supplies and medications from storerooms. Finding each item takes time away from treatment, and a missed or wrong item can delay a procedure. We created a tool that gets nurses through the storeroom faster and makes sure nothing is missed.

## What it does
**MedRoute** is smart inventory mapping for medical procedure prep.

- **Procedure requirements:**  Given a procedure, MedRoute calculates the optimal pick-up path in the equipment storeroom.
- **E-paper guidance:** A display on the device shows the next item needed, its location (aisle and shelf), and tells the User which way to go.
- **Barcode verification:** Scanning an item checks it off and moves to the next one. A repeated or wrong scan will notify the nurse.

## How we built it
- **Raspberry Pi 5** runs the routing logic and drives a **Waveshare 3.97" e-Paper HAT+**, which displays information about the needed items and what order to get them in.

- A **barcode scanner** confirms each item pick-up.
- The storeroom is modeled as a graph, where each vertex is a shelf location and each edge weight is the walking distance between two locations. For each procedure, we look for the visiting order of its required items that minimizes total distance.

## Challenges we ran into
- **Hardware limits:** The available hardware was very limited, so we had to design around the components that were available, often reevaluating ideas in the process.
- **E-paper refresh time:** E-paper redraws slowly, so we kept each screen simple and update it only when all the items are scanned. 

## Accomplishments that we're proud of
- On the software side, our optimizing algorithm was interesting to code, and we had to decide how to conduct the simulation in a way that would mimic real life.
- On the hardware side, our use of the e-paper display was both challenging and rewarding when we finally got it to work. 

## What we learned
- How to tie the routing, display, and scanner together into one workflow
- Applications of the Raspberry Pi 5 with displays and external input devices (barcode scanner, RFID reader)

## What's next for MedRoute
- Integration of multiple procedures per patient, automatically selected by prioritization and regularity of administration
- Live inventory numbers and low-stock alerts
- Refining the display and route logic: for example, implementing the Floyd-Warshall algorithm to find the best path through the warehouse
