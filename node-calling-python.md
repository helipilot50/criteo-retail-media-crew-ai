# Node Calling Python

When using the `node-calls-python` package, the Python script runs directly in-process with Node.js, which means it does not spawn a new process for each call. This approach minimizes overhead and can improve performance compared to traditional methods that involve inter-process communication (IPC) via sockets or stdin/stdout¹².

However, whether the Python script blocks the Node.js application until completion depends on how you call the Python function:

1. **Asynchronous Call**: If you use the asynchronous method (`py.call`), the Node.js application will not be blocked. The call will return a promise, allowing other operations to continue while waiting for the Python function to complete.
    ```javascript
    const nodecallspython = require("node-calls-python");
    const py = nodecallspython.interpreter;

    py.import("path/to/test.py").then(async function(pymodule) {
        const result = await py.call(pymodule, "function_name", arg1, arg2);
        console.log(result);
    });
    ```

2. **Synchronous Call**: If you use the synchronous method (`py.callSync`), the Node.js application will be blocked until the Python function completes. This method is useful for simpler tasks where blocking is acceptable.
    ```javascript
    const nodecallspython = require("node-calls-python");
    const py = nodecallspython.interpreter;

    py.import("path/to/test.py").then(function(pymodule) {
        const result = py.callSync(pymodule, "function_name", arg1, arg2);
        console.log(result);
    });
    ```

For most use cases, especially in a production environment, it's recommended to use the asynchronous method to keep your Node.js application responsive.


- [npm node-calls-python](https://www.npmjs.com/package/node-calls-python)
- [GitHub - node-calls-python](https://github.com/hmenyus/node-calls-python)

