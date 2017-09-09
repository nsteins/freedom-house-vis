var data = source.data;
var filetext = 'Country,Status,PR.Rating,CL.Rating,A1,A2,A3,A.Aggr,B1,B2,B3,B4,B.Aggr,C1,C2,C3,C.Aggr,Add.A,Add.B,PR.Aggr,D1,D2,D3,D4,D.Aggr,E1,E2,E3,E.Aggr,F1,F2,F3,F4,F.Aggr,G1,G2,G3,G4,G.Aggr,CL.Aggr,Total.Aggr,Year,Region,FSI_Total,FSI_Demographic.Pressures,FSI_Refugees.and.IDPs,FSI_Group.Grievance,FSI_Human.Flight,FSI_Uneven.Development,FSI_Poverty.and.Economic.Decline,FSI_Legitimacy.of.the.State,FSI_Public.Services,FSI_Human.Rights,FSI_Security.Apparatus,FSI_Factionalized.Elites,PTS_A,PTS_H,PTS_S,UN_hdi,UN_gdi,UN_gii,UN_iie,UN_iii,UN_iile,UN_imr,UN_ynis,UN_yu,TI_Corruption_Perception_Index,Ease.of.doing.business.index..1.most.business.friendly.regulations.,Fuel.exports....of.merchandise.exports.,GDP.at.market.prices..constant.2010.US..,GDP.growth..annual...,GDP.per.capita..constant.2010.US..,GDP..PPP..constant.2011.international...,Income.share.held.by.fourth.20.,Income.share.held.by.highest.10.,Income.share.held.by.highest.20.,Income.share.held.by.lowest.10.,Income.share.held.by.lowest.20.,Income.share.held.by.second.20.,Income.share.held.by.third.20.,Internally.displaced.persons..number..high.estimate.,Internally.displaced.persons..number..low.estimate.,Labor.force.participation.rate.for.ages.15.24..total......modeled.ILO.estimate.,Labor.force.participation.rate.for.ages.15.24..total......national.estimate.,Labor.force.participation.rate..total....of.total.population.ages.15....modeled.ILO.estimate.,Labor.force.participation.rate..total....of.total.population.ages.15....national.estimate.,Labor.force..female....of.total.labor.force.,Labor.force..total,Life.expectancy.at.birth..total..years.,Lifetime.risk.of.maternal.death....,Literacy.rate..adult.female....of.females.ages.15.and.above.,Literacy.rate..adult.male....of.males.ages.15.and.above.,Military.expenditure....of.GDP.,Mineral.rents....of.GDP.,Mobile.cellular.subscriptions..per.100.people.,Mortality.rate..under.5..per.1.000.live.births.,Net.bilateral.aid.flows.from.DAC.donors..Total..current.US..,Population.density..people.per.sq..km.of.land.area.,Population.growth..annual...,Population..total,Rural.population....of.total.population.\n';

for (i=0; i < data['Country'].length; i++) {
    var currRow = [ data['Country'][i].toString(),
                    data['Status'][i].toString(),
                    data['PR.Rating'][i].toString(),
                    data['CL.Rating'][i].toString(),
                    data['A1'][i].toString(),
                    data['A2'][i].toString(),
                    data['A3'][i].toString(),
                    data['A.Aggr'][i].toString(),
                    data['B1'][i].toString(),
                    data['B2'][i].toString(),
                    data['B3'][i].toString(),
                    data['B4'][i].toString(),
                    data['B.Aggr'][i].toString(),
                    data['C1'][i].toString(),
                    data['C2'][i].toString(),
                    data['C3'][i].toString(),
                    data['C.Aggr'][i].toString(),
                    data['Add.A'][i].toString(),
                    data['Add.B'][i].toString(),
                    data['PR.Aggr'][i].toString(),
                    data['D1'][i].toString(),
                    data['D2'][i].toString(),
                    data['D3'][i].toString(),
                    data['D4'][i].toString(),
                    data['D.Aggr'][i].toString(),
                    data['E1'][i].toString(),
                    data['E2'][i].toString(),
                    data['E3'][i].toString(),
                    data['E.Aggr'][i].toString(),
                    data['F1'][i].toString(),
                    data['F2'][i].toString(),
                    data['F3'][i].toString(),
                    data['F4'][i].toString(),
                    data['F.Aggr'][i].toString(),
                    data['G1'][i].toString(),
                    data['G2'][i].toString(),
                    data['G3'][i].toString(),
                    data['G4'][i].toString(),
                    data['G.Aggr'][i].toString(),
                    data['CL.Aggr'][i].toString(),
                    data['Total.Aggr'][i].toString(),
                    data['Year'][i].toString(),
                    data['Region'][i].toString(),
                    data['FSI_Total'][i].toString(),
                    data['FSI_Demographic.Pressures'][i].toString(),
                    data['FSI_Refugees.and.IDPs'][i].toString(),
                    data['FSI_Group.Grievance'][i].toString(),
                    data['FSI_Human.Flight'][i].toString(),
                    data['FSI_Uneven.Development'][i].toString(),
                    data['FSI_Poverty.and.Economic.Decline'][i].toString(),
                    data['FSI_Legitimacy.of.the.State'][i].toString(),
                    data['FSI_Public.Services'][i].toString(),
                    data['FSI_Human.Rights'][i].toString(),
                    data['FSI_Security.Apparatus'][i].toString(),
                    data['FSI_Factionalized.Elites'][i].toString(),
                    data['PTS_A'][i].toString(),
                    data['PTS_H'][i].toString(),
                    data['PTS_S'][i].toString(),
                    data['UN_hdi'][i].toString(),
                    data['UN_gdi'][i].toString(),
                    data['UN_gii'][i].toString(),
                    data['UN_iie'][i].toString(),
                    data['UN_iii'][i].toString(),
                    data['UN_iile'][i].toString(),
                    data['UN_imr'][i].toString(),
                    data['UN_ynis'][i].toString(),
                    data['UN_yu'][i].toString(),
                    data['TI_Corruption_Perception_Index'][i].toString(),
                    data['Ease.of.doing.business.index..1.most.business.friendly.regulations.'][i].toString(),
                    data['Fuel.exports....of.merchandise.exports.'][i].toString(),
                    data['GDP.at.market.prices..constant.2010.US..'][i].toString(),
                    data['GDP.growth..annual...'][i].toString(),
                    data['GDP.per.capita..constant.2010.US..'][i].toString(),
                    data['GDP..PPP..constant.2011.international...'][i].toString(),
                    data['Income.share.held.by.fourth.20.'][i].toString(),
                    data['Income.share.held.by.highest.10.'][i].toString(),
                    data['Income.share.held.by.highest.20.'][i].toString(),
                    data['Income.share.held.by.lowest.10.'][i].toString(),
                    data['Income.share.held.by.lowest.20.'][i].toString(),
                    data['Income.share.held.by.second.20.'][i].toString(),
                    data['Income.share.held.by.third.20.'][i].toString(),
                    data['Internally.displaced.persons..number..high.estimate.'][i].toString(),
                    data['Internally.displaced.persons..number..low.estimate.'][i].toString(),
                    data['Labor.force.participation.rate.for.ages.15.24..total......modeled.ILO.estimate.'][i].toString(),
                    data['Labor.force.participation.rate.for.ages.15.24..total......national.estimate.'][i].toString(),
                    data['Labor.force.participation.rate..total....of.total.population.ages.15....modeled.ILO.estimate.'][i].toString(),
                    data['Labor.force.participation.rate..total....of.total.population.ages.15....national.estimate.'][i].toString(),
                    data['Labor.force..female....of.total.labor.force.'][i].toString(),
                    data['Labor.force..total'][i].toString(),
                    data['Life.expectancy.at.birth..total..years.'][i].toString(),
                    data['Lifetime.risk.of.maternal.death....'][i].toString(),
                    data['Literacy.rate..adult.female....of.females.ages.15.and.above.'][i].toString(),
                    data['Literacy.rate..adult.male....of.males.ages.15.and.above.'][i].toString(),
                    data['Military.expenditure....of.GDP.'][i].toString(),
                    data['Mineral.rents....of.GDP.'][i].toString(),
                    data['Mobile.cellular.subscriptions..per.100.people.'][i].toString(),
                    data['Mortality.rate..under.5..per.1.000.live.births.'][i].toString(),
                    data['Net.bilateral.aid.flows.from.DAC.donors..Total..current.US..'][i].toString(),
                    data['Population.density..people.per.sq..km.of.land.area.'][i].toString(),
                    data['Population.growth..annual...'][i].toString(),
                    data['Population..total'][i].toString(),
                    data['Rural.population....of.total.population.'][i].toString().concat('\n')];

    var joined = currRow.join();
    filetext = filetext.concat(joined);
}

var filename = 'data_result.csv';
var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename);
}

else {
    var link = document.createElement("a");
    link = document.createElement('a')
    link.href = URL.createObjectURL(blob);
    link.download = filename
    link.target = "_blank";
    link.style.visibility = 'hidden';
    link.dispatchEvent(new MouseEvent('click'))
}