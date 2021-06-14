import React, { useState, useEffect } from "react";
import { fetchModel0 } from "./api";

export const App = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchModel0().then((data) => setData(data))
  }, []);

  if (data.length < 1) return <h1 style={{display:'flex',alignItems:'center',justifyContent:'center'}}>No data provided...</h1>;

  return (
    <div style={{display:'flex',alignItems:'center',justifyContent:'center'}}>
      {data.map((dataObj) => (
        <div>
          <h2>Name: {dataObj.name}</h2>
          <h2>Description: {dataObj.description}</h2>
          <h2>Value: {dataObj.value}</h2>
        </div>
      ))}
    </div>
  );
};

export default App;