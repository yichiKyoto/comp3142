
In the setup phase of the result_collector fixture, I wrote length,width,height,result into the CSV file
as shown here:  
with open(RESULT_FILE, "w", newline="") as f:
        f.write("length,width,height,result\n")

In the teardown phase, I write everything in records into the CSV file as shown here:
 with open(RESULT_FILE, "a", newline="") as f:
        for record in records:
            f.write(f"{record['length']},{record['width']},{record['height']},{record['result']}\n")
The records list consists of dictionaries where each dictonary has the keys length, width, height and result.

To implement the mocker that patches the check_price method, I created an additional function called fake_check_price,
which returns "543.21" if any dimension of the suitcase is greater than 500 and 124.45 otherwise. I replaced the check_price
method with this and created two suitcase objects which test the "mocked" implementation.

For testing gate1 and gate2, I created a fit suitcase and an unfit suitcase, called the can_pass_gate function on both of them,
before appending them to the result_collector list to write all results into the csv file. The results would include
the length of the suitcase, the width of the suitcase, the height of the suitcase and whether the suitcase can fit.

