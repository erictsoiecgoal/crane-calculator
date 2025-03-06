# crane-calculator

## pre-requisite
Flask, numpy, matplotlib

## run
`python main.py`

## call on cURL

`curl --location 'http://localhost:5000/plot_crane_img' \
--header 'Content-Type: application/json' \
--data '{
    "boomLength": 57.8,
    "boomAngleRad": 1.5,
    "boomAngleDeg": 85.943669
}'`

* Note: Replace localhost with 192.xxx.xxx.xxx ip address depending on the log. Example:
  ![image](https://github.com/user-attachments/assets/4bc954d3-aa1b-4bed-8315-4a41e5a3974f)

* Sample response (after decoding the base64 string):
  ![image](https://github.com/user-attachments/assets/bdfd34ca-393b-4512-b4a2-5964e808e05b)

## Integration with n8n

* Refer to `My_workflow.json` for the n8n workflow. After deploying the Python Flask server and importing the n8n json, the workflow should be functioning properly.

![image](https://github.com/user-attachments/assets/3053369a-37fb-4920-98a9-07b7473e6e82)

![image](https://github.com/user-attachments/assets/0d185e9d-382a-49ae-8b02-b28dedb7f71b)

* Note: Use the following code in the code block before the POST request:
  `const radius = Math.abs($input.first().json.Radius);
const load = Math.abs($input.first().json.Load) + 0.4;
const boomLength = radius * (1 + load / 10);
const boomAngleRad = Math.acos(radius / boomLength);
const boomAngleDeg = boomAngleRad * (180 / Math.PI);
return { boomLength, boomAngleRad, boomAngleDeg };`
