import axios from 'axios';

const WEB_SERVER = process.env.REACT_APP_WEB_SERVER_URL;

export const helloWorld = async () => {
  const response = await axios.get(WEB_SERVER + '/hello');
  return response;
};
