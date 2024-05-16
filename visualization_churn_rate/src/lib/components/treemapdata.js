export default function convertToTreemapData(data) {
    const treemapData = {
      name: `${data.Year}-${data.Month}`,
      children: Object.keys(data)
        .filter(key => key.startsWith('ADVENTURING EQUIPMENT_') || key.startsWith('TOOLS & KITS_') || key.startsWith('POTIONS & SCROLLS_') || key.startsWith('ANIMALS & TRANSPORTATION_') || key.startsWith('JEWELRY_') || key.startsWith('SUMMONING DEVICE_') || key.startsWith('MUSICAL INSTRUMENT_'))
        .map(key => {
          const category = key.replace('_Percentage', '');
          return {
            name: category,
            value: data[key]
          };
        })
    };
    return treemapData;
  }