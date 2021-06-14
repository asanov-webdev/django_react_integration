import axios from "./axios-config";

export async function fetchModel0() {
  const data = await axios.get("/app0/").then((response) => response.data);

  return data;
}

