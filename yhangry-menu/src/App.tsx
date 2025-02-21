import { useState } from "react";
import "./App.css";
import { useMenuQueries } from "./hooks/useMenuQueries";
import type { Cuisine, Menu } from "./hooks/useMenuQueries";
function App() {
  const [selectedCuisine, setSelectedCuisine] = useState<string | null>(null);
  const [guests, setGuests] = useState<number>(1);

  const {
    menus,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    cuisines,
  } = useMenuQueries(selectedCuisine);

  const calculateTotal = (price: number, min: number): number =>
    Math.max(price * guests, min);

  if (isLoading) return <div>Loading...</div>;

  const handleLoadMore = async () => {
    try {
      await fetchNextPage();
    } catch (error) {
      console.error("Failed to load more:", error);
    }
  };

  return (
    <div className="container">
      <div className="filters">
        <input
          type="number"
          min="1"
          value={guests}
          onChange={(e) => setGuests(Math.max(1, Number(e.target.value)))}
          placeholder="Number of guests"
        />
        {cuisines.map((cuisine: Cuisine) => (
          <button
            key={cuisine.id}
            onClick={() => setSelectedCuisine(cuisine.name)}
            className={selectedCuisine === cuisine.name ? "active" : ""}
          >
            {cuisine.name} ({cuisine.menu_count})
          </button>
        ))}
      </div>

      <div className="menu-grid">
        {menus?.map((menu: Menu) => (
          <div key={menu.id} className="menu-card">
            <img src={menu.image} alt={menu.name} />
            <h3>{menu.name}</h3>
            <p>{menu.description}</p>
            <div className="price">
              Total: £{calculateTotal(menu.price_per_person, menu.min_spend)}
              <small>(£{menu.price_per_person} per person)</small>
            </div>
            <div className="cuisines">
              {menu.cuisines.map((c) => (
                <span key={c.id} className="cuisine-tag">
                  {c.name}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>

      {hasNextPage && (
        <button
          onClick={handleLoadMore}
          disabled={isFetchingNextPage}
          className="load-more"
        >
          {isFetchingNextPage ? "Loading more..." : "Load More"}
        </button>
      )}
    </div>
  );
}

export default App;
