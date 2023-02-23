import axios from 'axios';

export default axios.create({
  baseURL: 'http://localhost:9393',
  responseType: 'json',
  headers: { 'Access-Control-Allow-Origin': '*' },
});
