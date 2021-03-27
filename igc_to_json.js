const fs = require('fs')
const IGCParser = require('igc-parser')

if (process.argv.length < 3) {
  console.error('wrong usage, use: in_file')
  process.exit(1)
}

const inFile = process.argv[2]

parse(inFile)

function parse(inFile, outFile) {
  const inBytes = fs.readFileSync(inFile, 'utf8')
  let result = IGCParser.parse(inBytes, { lenient: true })

  process.stdout.write(JSON.stringify(result))
}
