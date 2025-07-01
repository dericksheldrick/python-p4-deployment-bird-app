import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function BirdDetail() {
  let { id } = useParams();
  const [bird, setBird] = useState({});

  useEffect(() => {
    fetch(`/api/birds/${id}`)
      .then((r) => r.json())
      .then((bird) => setBird(bird));

    return () => setBird({});
  }, [id]);

  const { name, species, image } = bird;

  const [isInStock, setIsInStock] = useState(true);

  function handleToggleStock() {
    setIsInStock((isInStock) => !isInStock);
  }

  return (
    <div className="details">
      <img src={image} alt={name} />

      <h4>{name}</h4>
      <p>Species: {species}</p>
      {isInStock ? (
        <button className="primary" onClick={handleToggleStock}>
          Available for Events
        </button>
      ) : (
        <button onClick={handleToggleStock}>Fully Booked</button>
      )}
    </div>
  );
}

export default BirdDetail;
