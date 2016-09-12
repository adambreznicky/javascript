// index.js

// require('./app/index')

// const http = require('http')  
// const port = 3000

// const requestHandler = (request, response) => {  
//   console.log(request.url)
//   response.end('Hello Node.js Server!')
// }

// const server = http.createServer(requestHandler)

// server.listen(port, (err) => {  
//   if (err) {
//     return console.log('something bad happened', err)
//   }

//   console.log(`server is listening on ${port}`)
// })


const path = require('path')  
const express = require('express')  
const exphbs = require('express-handlebars')
const app = express()


// app.use((request, response, next) => {  
//   console.log(request.headers)
//   next()
// })

// app.use((request, response, next) => {  
//   request.chance = Math.random()
//   next()
// })

// app.get('/', (request, response) => {  
//   response.json({
//     chance: request.chance
//   })
// })
//-------------------------------------------------
// app.engine('.hbs', exphbs({  
//   defaultLayout: 'main',
//   extname: '.hbs',
//   layoutsDir: path.join(__dirname, 'views/layouts')
// }))
// app.set('view engine', '.hbs')  
// app.set('views', path.join(__dirname, 'views'))  
app.use(express.static('./app'));
app.use('angular', express.static('./node_modules/angular'));

app.get('/', function (request, response) {  
  // response.render('home', {
  //   name: 'Brez'
  // })
  response.sendFile('/home/ubuntu/workspace/node/index.html');
  // console.log(response);
})

app.listen(process.env.PORT)  
