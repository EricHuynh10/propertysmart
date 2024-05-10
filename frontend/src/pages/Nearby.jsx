import React, { useEffect, useState } from "react";

const Nearby = () => {
  const [location, setLocation] = useState(null);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        setLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
      });
      console.log('location', location)
    } else {
      console.log("Geolocation is not supported by this browser.");
    }
  }, []);

  return (
    <div>
      Nearby
      {location && (
        <div>
          Latitude: {location.latitude}, Longitude: {location.longitude}
        </div>
      )}
    </div>
  );
};

export default Nearby;