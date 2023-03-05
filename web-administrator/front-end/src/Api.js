import axios from "axios";

export default axios.create({
    baseURL: "http://34.133.64.76:8181",
    responseType: "json",
    headers : {"Access-Control-Allow-Origin": "*"}
});