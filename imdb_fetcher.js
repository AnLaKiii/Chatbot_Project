const fs = require('fs');
const axios = require('axios');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

const TMDB_API_KEY = 'b6d8820d3664aebe1365bda62991baf9';
const OUTPUT_CSV = 'film_verisi.csv';

const csvWriter = createCsvWriter({
  path: OUTPUT_CSV,
  header: [
    { id: 'film_title', title: 'film_title' },
    { id: 'category', title: 'category' },
    { id: 'plot', title: 'plot' }
  ],
  append: false
});

let genreMap = {};

async function fetchGenreMap() {
  const url = `https://api.themoviedb.org/3/genre/movie/list?api_key=${TMDB_API_KEY}&language=tr-TR`;
  const res = await axios.get(url);
  res.data.genres.forEach(g => {
    genreMap[g.id] = g.name;
  });
}

function isLatin(text) {
  // Latin harfleri dışındaki karakterleri tespit et
  return /^[\x00-\x7F]+$/.test(text) || /^[a-zA-Z0-9ğüşıöçĞÜŞİÖÇ\s.,:;'"!?()\-]+$/.test(text);
}

async function fetchPopularMovies() {
  await fetchGenreMap();
  const films = [];

  for (let page = 1; page <= 100; page++) {
    const url = `https://api.themoviedb.org/3/movie/popular?api_key=${TMDB_API_KEY}&language=tr-TR&page=${page}`;

    try {
      const res = await axios.get(url);

      if (!res.data || !res.data.results) {
        console.warn(`⚠️ Sayfa ${page} boş.`);
        continue;
      }

      res.data.results.forEach(movie => {
        const plot = movie.overview?.trim();
        const title = movie.title?.trim();

        // 1. Film adı Latin karakterli değilse atla
        if (!isLatin(title)) return;

        // 2. Konu boşsa atla
        if (!plot || plot.length < 10) return;

        const turkceTurler = (movie.genre_ids || [])
          .map(id => genreMap[id])
          .filter(Boolean)
          .join(', ');

        films.push({
          film_title: title,
          category: turkceTurler || 'Bilinmiyor',
          plot: plot
        });
      });

      console.log(`✅ Sayfa ${page} işlendi (${res.data.results.length} film incelendi)`);

    } catch (err) {
      console.error(`❌ Sayfa ${page} hata:`, err.response?.data || err.message);
      break;
    }
  }

  console.log(`📊 Uygun bulunan film sayısı: ${films.length}`);

  if (films.length > 0) {
    await csvWriter.writeRecords(films);
    console.log(`📁 film_verisi.csv dosyasına yazıldı.`);
  } else {
    console.warn('⚠️ Yazılacak uygun film bulunamadı.');
  }
}

fetchPopularMovies();
