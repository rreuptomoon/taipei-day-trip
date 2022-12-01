
let loading = false;


loadData(0, "");
loadCategories();



let nextpage;
let keyword;


async function loadData(page, keyword) {
  loading = true;

  let taipeiAPI = await fetch(`/api/attractions?page=${page}&keyword=${keyword}`);
  let taipeiData = await taipeiAPI.json();
  getData(taipeiData);
  nextpage = taipeiData.nextpage;
  // console.log(nextpage);
  // console.log(keyword);

  loading = false;
}

function getData(taipeiData) {

const MainContent = document.querySelector(".main-content");
  // console.log(taipeiData.data);

  let data = taipeiData.data;

   let ContentBox = document.createElement("div")
  ContentBox.classList.add("content")

  if (data.length === 0) {
    loading = true;
    ContentBox.innerHTML = "<div class='no-data'> sorry ! non result </div>";
  }

  loading = true;

  for (let res of data) {
    ContentBox.innerHTML += `
             <div class="photo">
            <a href="">
              <img src="${res.images[0]}" alt="" />
              <span>${res.name}</span>
            </a>
            <div class="photo-down">
              <p>${res.mrt}</p>
              <p>${res.category}</p>
            </div>
          </div>
           `;
  }
  MainContent.appendChild(ContentBox);

};

/* scrollPage */
let target = document.querySelector('footer');

 const options = {
    root :null,
    rootMargin : "50px",
    threshold : 1,
 };

const scrollPage = (entries,observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting){
            if(nextpage != null && loading == false){
                if(!keyword){
                    loadData(nextpage,"");
                }else{
                    loadData(nextpage,keyword);
                }
            }
        }
    })
};
const observer = new IntersectionObserver(scrollPage, options);
observer.observe(target);



//search keyword:
const MainContent = document.querySelector(".main-content");
const Search = document.querySelector(".search")
const SearchBar = document.getElementById("search-bar");
const SearchBtn = document.getElementById("search-btn");
SearchBtn.addEventListener("click", function () {
    keyword = SearchBar.value;
    SearchBar.value = "";
    MainContent.innerHTML = "";
    loadData(0, keyword);
})
 


/* search bar */
async function loadCategories() {
  loading = true;
  let categoriesApi = await fetch("http://13.251.71.73:3000//api/categories");
  let categoryData = await categoriesApi.json();
  getCat(categoryData)
  // console.log(categoryData.data);
  loading = false;

};

const Catlist = document.querySelector(".cat-list");
function getCat(categoryData) {
  let category = categoryData.data;
  console.log(category[0]);

  for (let i = 0; i < category.length; i++){
    let CatData = document.createElement("div");
    CatData.classList.add("cat");
    CatData.innerText = category[i];
    Catlist.appendChild(CatData);
  }
};



SearchBar.addEventListener("click", function () {
  Catlist.style.display = "block";
  
const catlistAllcat = document.querySelectorAll(".cat");
  for (let i = 0; i < catlistAllcat.length; i++){
    catlistAllcat[i].addEventListener("click", function () {
    
      SearchBar.value = catlistAllcat[i].innerText;

      // console.log(SearchBar.value);
      Catlist.style.display = "none"
    })
    
  }
  
});









