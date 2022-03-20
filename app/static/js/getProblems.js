problems = {
	mech: {},
	kinematics: {},
	em: {},
	thermo: {},
	waves: {},
	modern: {},
}

function tabulate(location, data, columns) {
	var table = d3.select(`#${location}`).html('').append('table').attr('class', 'table');
	var thead = table.append('thead');
	var	tbody = table.append('tbody');

	// append the header row
	thead.append('tr')
	  .selectAll('th')
	  .data(columns).enter()
	  .append('th')
	    .text(function (column) { return column; })
			.attr('scope', 'col');

	// create a row for each object in the data
	var rows = tbody.selectAll('tr')
	  .data(data)
	  .enter()
	  .append('tr');

	// create a cell in each row for each column
	var cells = rows.selectAll('td')
	  .data(function (row) {
	    return columns.map(function (column) {
	      return {column: column, value: row[column]};
	    });
	  })
	  .enter()
	  .append('td')
	    .text(function (d) { return d.value; });

  return table;
}

d3.csv('/static/csv/mech.csv', data => {
	problems.mech = data;
	tabulate('mechData', problems.mech, ['Problem Name', 'Rating', 'Difficulty', 'Length', 'Description']);
});

d3.csv('/static/csv/kinematics.csv', data => {
	problems.kinematics = data;
	tabulate('kinData', problems.mech, ['Problem Name', 'Rating', 'Difficulty', 'Length', 'Description']);
});

d3.csv('/static/csv/em.csv', data => {
	problems.em = data;
	tabulate('emData', problems.mech, ['Problem Name', 'Rating', 'Difficulty', 'Length', 'Description']);
});

d3.csv('/static/csv/thermo.csv', data => {
	problems.thermo = data;
	tabulate('thermoData', problems.mech, ['Problem Name', 'Rating', 'Difficulty', 'Length', 'Description']);
});

d3.csv('/static/csv/waves.csv', data => {
	problems.waves = data;
	tabulate('waveData', problems.mech, ['Problem Name', 'Rating', 'Difficulty', 'Length', 'Description']);
});

d3.csv('/static/csv/modern.csv', data => {
	problems.modern = data;
	tabulate('modernData', problems.mech, ['Problem Name', 'Rating', 'Difficulty', 'Length', 'Description']);
});


