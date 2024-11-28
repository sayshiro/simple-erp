const mongoose = require('mongoose');
const MetalType = require('./models/MetalType');
const MetalGost = require('./models/MetalGost');
const MetalGrade = require('./models/MetalGrade');

mongoose.connect('mongodb://localhost:27017/erp', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', async function() {
  console.log('Connected to MongoDB');

  // Step 1: Add metal types
  const types = [
    { name: 'Лист' },
    { name: 'Труба круглая' },
    { name: 'Труба профильная' },
    { name: 'Уголок' },
    { name: 'Швеллер' }
  ];
  await MetalType.insertMany(types);
  console.log('Metal types added');

  // Step 2: Add GOSTs
  const gosts = [
    { number: '19903-2015', name: 'Прокат листовой горячекатаный' },
    { number: '10704-91', name: 'Трубы стальные электросварные прямошовные' },
    { number: '8639-82', name: 'Трубы стальные квадратные' },
    { number: '8509-93', name: 'Уголки стальные горячекатаные равнополочные' },
    { number: '8240-97', name: 'Швеллеры стальные горячекатаные' }
  ];
  await MetalGost.insertMany(gosts);
  console.log('GOSTs added');

  // Step 3: Add metal grades
  const grades = [
    { name: 'Ст3', description: 'Углеродистая сталь обыкновенного качества' },
    { name: '09Г2С', description: 'Низколегированная конструкционная сталь' },
    { name: '20', description: 'Конструкционная углеродистая качественная сталь' },
    { name: '45', description: 'Конструкционная углеродистая качественная сталь' },
    { name: '40Х', description: 'Легированная конструкционная сталь' }
  ];
  await MetalGrade.insertMany(grades);
  console.log('Metal grades added');

  mongoose.connection.close();
});
