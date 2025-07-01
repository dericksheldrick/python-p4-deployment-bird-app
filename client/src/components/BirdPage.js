import { useEffect, useState } from "react";
import NewBirdForm from "./NewBirdForm";
import BirdList from "./BirdList";
import Search from "./Search";

function BirdPage() {
  const [birds, setBirds] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetch("/api/birds")
      .then((r) => r.json())
      .then((birdsArray) => {
        setBirds(birdsArray);
      });
  }, []);

  function handleAddBird(newBird) {
    const updatedBirdsArray = [...birds, newBird];
    setBirds(updatedBirdsArray);
  }

  const displayedBirds = birds.filter((bird) => {
    return bird.name.toLowerCase().includes(searchTerm.toLowerCase());
  });

if(!birds) return <h1>...loading</h1>

  return (
    <main>
      <NewBirdForm onAddBird={handleAddBird} />
      <Search searchTerm={searchTerm} onSearchChange={setSearchTerm} />
      <BirdList birds={displayedBirds} />
    </main>
  );
}

export default BirdPage;
