import CustomCards from "../shared/CustomCards";

export default function CardsSection() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-5 mt-10">
      {Array.from({ length: 8 }).map((_, i) => (
        <CustomCards key={i} />
      ))}
    </div>
  );
}
