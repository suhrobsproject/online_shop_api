import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api";

const client = axios.create({
  baseURL: API_URL,
});

export default client;
