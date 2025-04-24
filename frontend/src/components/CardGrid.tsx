
import GameCard from "./GameCard";

const CardGrid = () => {
  const cards = [
    {
      title: "Level 1",
      description: "Begin your journey here",
    },
    {
      title: "Level 2",
      description: "Test your skills",
    },
    {
      title: "Level 3",
      description: "Advanced challenges await",
    },
    {
      title: "Level 4",
      description: "Master level",
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-6 p-6 sm:grid-cols-2 lg:grid-cols-4">
      {cards.map((card, index) => (
        <GameCard
          key={index}
          title={card.title}
          description={card.description}
        />
      ))}
    </div>
  );
};

export default CardGrid;
