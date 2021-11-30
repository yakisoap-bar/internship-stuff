const app = require('./controller/app');

// start server
let port = 3000;
app.listen(port, () => {console.log(`Server started on http://localhost:${port}`)});
