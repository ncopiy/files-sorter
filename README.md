# Files Sorter

Copies files from source directories to destination directory and sorts it by timestamp

Example of the expected result:

```
destination/
├─ 2017/
│  ├─ 04/
│  │  ├─ 05/
│  │  │  ├─ file created 05.04.2017
│  │  │  ├─ photo taken 05.04.2017
├─ 2022/
│  ├─ 12/
│  │  ├─ 23/
│  │  │  ├─ photo taken 23.12.2022
```

[//]: # (Tip for future self: to find the DCIM dir connect iphone to linux, open dir and drop the `:3` from the path. the path to the DCIM dir will be something like `/run/user/1000/gvfs/afc:host=00008101-001169342261001E/DCIM`)
[//]: # (Tip for future self 2: drop the files from `recently deleted` folder to prevent handling)
